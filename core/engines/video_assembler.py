"""Video Assembler - Creates storyboards and video plans."""

from typing import List, Dict, Any, Optional
import logging

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import (
    Storyboard,
    StoryboardScene,
    Script,
    ContentFormat,
)


logger = get_logger(__name__)


class VideoAssembler(BaseEngine):
    """Assembles video components into storyboards and production plans."""
    
    def __init__(self):
        super().__init__("video_assembler")
    
    async def assemble(
        self,
        script: Script,
        format_type: ContentFormat,
        style_notes: str = "",
    ) -> Storyboard:
        """Create a storyboard from a script.
        
        Args:
            script: Complete video script
            format_type: Content format
            style_notes: Optional style notes
            
        Returns:
            Complete Storyboard object
        """
        try:
            self.logger.info(f"Assembling storyboard for: {script.title}")
            
            scenes = await self._create_scenes_from_script(script, format_type)
            
            total_duration = sum(s.duration_seconds for s in scenes)
            
            return Storyboard(
                title=script.title,
                scenes=scenes,
                total_duration_seconds=total_duration,
                style_notes=style_notes or f"Style for {format_type.value} format",
            )
            
        except Exception as e:
            self.logger.error(f"Error assembling storyboard: {e}")
            return self._fallback_storyboard(script)
    
    async def _create_scenes_from_script(
        self,
        script: Script,
        format_type: ContentFormat,
    ) -> List[StoryboardScene]:
        """Create storyboard scenes from script sections.
        
        Args:
            script: Video script
            format_type: Content format
            
        Returns:
            List of StoryboardScene objects
        """
        scenes = []
        scene_number = 1
        
        for section in script.sections:
            # Create one or more scenes per section based on duration
            if section.duration_seconds > 120:
                # Split long sections into multiple scenes
                num_scenes = section.duration_seconds // 60
                segment_duration = section.duration_seconds // num_scenes
                
                for i in range(num_scenes):
                    scene = await self._create_scene(
                        section,
                        scene_number,
                        segment_duration,
                        format_type,
                        i,
                        num_scenes,
                    )
                    scenes.append(scene)
                    scene_number += 1
            else:
                scene = await self._create_scene(
                    section,
                    scene_number,
                    section.duration_seconds,
                    format_type,
                )
                scenes.append(scene)
                scene_number += 1
        
        return scenes
    
    async def _create_scene(
        self,
        section,
        scene_number: int,
        duration: int,
        format_type: ContentFormat,
        part_index: int = 0,
        total_parts: int = 1,
    ) -> StoryboardScene:
        """Create a single storyboard scene.
        
        Args:
            section: Script section
            scene_number: Scene number
            duration: Scene duration
            format_type: Content format
            part_index: Part index if section is split
            total_parts: Total parts if section is split
            
        Returns:
            StoryboardScene object
        """
        # Generate visual prompt based on section content and format
        visual_prompt = await self._generate_visual_prompt(
            section.content,
            section.section_type,
            format_type,
            section.visual_cues if hasattr(section, 'visual_cues') else [],
        )
        
        # Generate audio prompt
        audio_prompt = self._generate_audio_prompt(
            section.content,
            section.section_type,
        )
        
        # Determine transition
        transition = self._get_transition(section.section_type, format_type)
        
        # Get assets needed
        assets_needed = self._get_assets_needed(
            section.section_type,
            format_type,
            visual_prompt,
        )
        
        return StoryboardScene(
            scene_number=scene_number,
            description=f"{section.section_type.capitalize()} - Part {part_index + 1}/{total_parts}" if total_parts > 1 else section.section_type.capitalize(),
            duration_seconds=duration,
            visual_prompt=visual_prompt,
            audio_prompt=audio_prompt,
            transition=transition,
            assets_needed=assets_needed,
        )
    
    async def _generate_visual_prompt(
        self,
        content: str,
        section_type: str,
        format_type: ContentFormat,
        visual_cues: List[str],
    ) -> str:
        """Generate visual prompt for a scene.
        
        Args:
            content: Script content
            section_type: Section type
            format_type: Content format
            visual_cues: Visual cues from script
            
        Returns:
            Visual prompt string
        """
        base_prompts = {
            "hook": "Engaging opening shot that grabs attention immediately",
            "intro": "Clear introduction with host or title graphics",
            "body": "Main content visualization with supporting graphics",
            "cta": "Call-to-action screen with subscribe/follow prompts",
        }
        
        base = base_prompts.get(section_type, content[:100])
        
        # Add format-specific elements
        format_additions = {
            ContentFormat.DOCUMENTARY: ", documentary-style cinematography, B-roll footage",
            ContentFormat.EXPLAINER: ", clean graphics, diagrams, screen captures",
            ContentFormat.STORYTELLING: ", cinematic composition, emotional lighting",
            ContentFormat.NEWS: ", news desk setup, lower thirds graphics",
            ContentFormat.SHORTS: ", vertical format, quick cuts, dynamic movement",
            ContentFormat.ANIMATION: ", animated characters, motion graphics",
            ContentFormat.MOTION_GRAPHICS: ", abstract shapes, data visualization",
        }
        
        addition = format_additions.get(format_type, "")
        
        # Add visual cues
        cues_str = ", ".join(visual_cues) if visual_cues else ""
        
        return f"{base}{addition}{', ' + cues_str if cues_str else ''}"
    
    def _generate_audio_prompt(
        self,
        content: str,
        section_type: str,
    ) -> str:
        """Generate audio direction for a scene.
        
        Args:
            content: Script content
            section_type: Section type
            
        Returns:
            Audio prompt string
        """
        audio_directions = {
            "hook": "Upbeat, attention-grabbing music. Clear, energetic voice.",
            "intro": "Welcome music fades in. Warm, friendly narration.",
            "body": "Background music at low volume. Clear narration with emphasis on key points.",
            "cta": "Upbeat outro music. Enthusiastic call-to-action voice.",
        }
        
        return audio_directions.get(section_type, "Narration with appropriate background music")
    
    def _get_transition(
        self,
        section_type: str,
        format_type: ContentFormat,
    ) -> str:
        """Get transition type for a scene.
        
        Args:
            section_type: Section type
            format_type: Content format
            
        Returns:
            Transition type
        """
        if section_type == "hook":
            return "fade_in"
        elif section_type == "cta":
            return "fade_out"
        elif format_type == ContentFormat.SHORTS:
            return "quick_cut"
        elif format_type in [ContentFormat.DOCUMENTARY, ContentFormat.STORYTELLING]:
            return "cross_dissolve"
        else:
            return "cut"
    
    def _get_assets_needed(
        self,
        section_type: str,
        format_type: ContentFormat,
        visual_prompt: str,
    ) -> List[str]:
        """Determine assets needed for a scene.
        
        Args:
            section_type: Section type
            format_type: Content format
            visual_prompt: Visual prompt
            
        Returns:
            List of asset descriptions
        """
        assets = []
        
        # Format-specific assets
        if format_type == ContentFormat.DOCUMENTARY:
            assets.extend(["B-roll footage", "Interview clips", "Archival material"])
        elif format_type == ContentFormat.EXPLAINER:
            assets.extend(["Screen captures", "Diagrams", "Icons"])
        elif format_type == ContentFormat.ANIMATION:
            assets.extend(["Character models", "Animated backgrounds", "Motion graphics"])
        
        # Section-specific assets
        if section_type == "hook":
            assets.append("Opening title graphic")
        elif section_type == "cta":
            assets.extend(["End screen template", "Subscribe button animation"])
        
        return assets
    
    def _fallback_storyboard(self, script: Script) -> Storyboard:
        """Generate fallback storyboard on error."""
        return Storyboard(
            title=script.title,
            scenes=[
                StoryboardScene(
                    scene_number=1,
                    description="Introduction",
                    duration_seconds=30,
                    visual_prompt="Opening shot",
                    audio_prompt="Intro music",
                ),
                StoryboardScene(
                    scene_number=2,
                    description="Main content",
                    duration_seconds=300,
                    visual_prompt="Content visualization",
                    audio_prompt="Narration",
                ),
                StoryboardScene(
                    scene_number=3,
                    description="Conclusion",
                    duration_seconds=30,
                    visual_prompt="Closing shot",
                    audio_prompt="Outro music",
                ),
            ],
            total_duration_seconds=360,
            style_notes="Fallback storyboard",
        )
    
    async def generate_video_plan(
        self,
        storyboard: Storyboard,
    ) -> Dict[str, Any]:
        """Generate a complete video production plan.
        
        Args:
            storyboard: Storyboard object
            
        Returns:
            Video production plan dictionary
        """
        all_assets = set()
        for scene in storyboard.scenes:
            all_assets.update(scene.assets_needed)
        
        return {
            "title": storyboard.title,
            "total_duration": storyboard.total_duration_seconds,
            "scene_count": len(storyboard.scenes),
            "assets_needed": list(all_assets),
            "production_notes": storyboard.style_notes,
            "scenes": [
                {
                    "number": s.scene_number,
                    "description": s.description,
                    "duration": s.duration_seconds,
                    "transition": s.transition,
                }
                for s in storyboard.scenes
            ],
        }
    
    async def process(self, *args, **kwargs) -> Storyboard:
        """Process video assembly request."""
        script = kwargs.get("script")
        format_type = kwargs.get("format_type", ContentFormat.EXPLAINER)
        style_notes = kwargs.get("style_notes", "")
        
        if not script:
            # Create minimal script for fallback
            from config.models import Script, ScriptSection
            script = Script(
                title="Untitled",
                topic="Untitled",
                format=format_type,
                sections=[ScriptSection(section_type="body", content="Content", duration_seconds=60)],
                total_duration_seconds=60,
                word_count=1,
            )
        
        return await self.assemble(script, format_type, style_notes)
