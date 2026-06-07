"""Thumbnail Engine - Generates thumbnail concepts and prompts."""

from typing import List, Dict, Any, Optional
import logging

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import ThumbnailConcept, ContentFormat


logger = get_logger(__name__)


class ThumbnailEngine(BaseEngine):
    """Generates thumbnail concepts, text, and AI image prompts."""
    
    def __init__(self):
        super().__init__("thumbnail_engine")
        self._format_styles = {
            ContentFormat.DOCUMENTARY: self._documentary_style,
            ContentFormat.EXPLAINER: self._explainer_style,
            ContentFormat.STORYTELLING: self._storytelling_style,
            ContentFormat.NEWS: self._news_style,
            ContentFormat.SHORTS: self._shorts_style,
            ContentFormat.ANIMATION: self._animation_style,
            ContentFormat.MOTION_GRAPHICS: self._motion_graphics_style,
            ContentFormat.HYBRID: self._hybrid_style,
            ContentFormat.CRIME_DOCUMENTARY: self._crime_style,
            ContentFormat.HISTORY_DOCUMENTARY: self._history_style,
        }
    
    async def generate(
        self,
        topic: str,
        format_type: ContentFormat = ContentFormat.EXPLAINER,
        target_audience: str = "general",
    ) -> ThumbnailConcept:
        """Generate a thumbnail concept for a video.
        
        Args:
            topic: Video topic
            format_type: Content format
            target_audience: Target audience
            
        Returns:
            ThumbnailConcept object
        """
        try:
            self.logger.info(f"Generating thumbnail for: {topic}")
            
            # Get style for format
            style_fn = self._format_styles.get(
                format_type, self._explainer_style
            )
            
            concept = await style_fn(topic, target_audience)
            
            # Generate AI prompt
            concept.prompt = await self.generate_prompt(concept)
            
            # Calculate CTR score (mock)
            concept.ctr_score = self._estimate_ctr(concept)
            
            return concept
            
        except Exception as e:
            self.logger.error(f"Error generating thumbnail: {e}")
            return self._fallback_thumbnail(topic)
    
    async def _documentary_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate documentary-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Dramatic documentary style with compelling imagery related to {topic}",
            main_text=self._generate_main_text(topic, 4),
            secondary_text="FULL DOCUMENTARY",
            color_scheme="Dark, moody with high contrast",
            mood="Serious, investigative",
            elements=[
                "Central subject image",
                "Dramatic lighting",
                "Bold title text",
                "Subtle texture overlay",
            ],
        )
    
    async def _explainer_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate explainer-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Clean, educational design explaining {topic}",
            main_text=self._generate_main_text(topic, 3),
            secondary_text="EXPLAINED",
            color_scheme="Bright, clean colors",
            mood="Friendly, approachable",
            elements=[
                "Clear central graphic",
                "Simple icon or illustration",
                "Bold readable text",
                "White or light background",
            ],
        )
    
    async def _storytelling_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate storytelling-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Emotional, narrative-driven thumbnail for {topic}",
            main_text=self._generate_main_text(topic, 4),
            secondary_text="THE STORY",
            color_scheme="Warm, cinematic tones",
            mood="Emotional, engaging",
            elements=[
                "Character or subject focus",
                "Cinematic composition",
                "Emotional expression",
                "Story hint in background",
            ],
        )
    
    async def _news_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate news-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Breaking news style for {topic}",
            main_text=self._generate_main_text(topic, 3),
            secondary_text="BREAKING",
            color_scheme="Red, white, blue - urgent colors",
            mood="Urgent, important",
            elements=[
                "Breaking news banner",
                "Anchor/host image",
                "Headline text",
                "Live indicator",
            ],
        )
    
    async def _shorts_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate Shorts-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Eye-catching vertical thumbnail for {topic}",
            main_text=self._generate_main_text(topic, 2),
            secondary_text="",
            color_scheme="Vibrant, bold colors",
            mood="Exciting, fast-paced",
            elements=[
                "Large expressive face or object",
                "Minimal text",
                "Bright background",
                "Emoji or graphic element",
            ],
        )
    
    async def _animation_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate animation-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Animated style thumbnail for {topic}",
            main_text=self._generate_main_text(topic, 3),
            secondary_text="ANIMATED",
            color_scheme="Colorful, playful palette",
            mood="Fun, creative",
            elements=[
                "Cartoon character or mascot",
                "Animated-style graphics",
                "Bold outlines",
                "Gradient backgrounds",
            ],
        )
    
    async def _motion_graphics_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate motion graphics-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Modern motion graphics style for {topic}",
            main_text=self._generate_main_text(topic, 3),
            secondary_text="VISUAL GUIDE",
            color_scheme="Modern gradients, neon accents",
            mood="Professional, tech-forward",
            elements=[
                "Abstract geometric shapes",
                "Data visualization elements",
                "Glowing effects",
                "Clean typography",
            ],
        )
    
    async def _hybrid_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate hybrid-style thumbnail."""
        return await self._explainer_style(topic, audience)
    
    async def _crime_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate crime documentary-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"True crime style thumbnail for {topic}",
            main_text=self._generate_main_text(topic, 4),
            secondary_text="CRIME FILES",
            color_scheme="Dark red, black, gray",
            mood="Mysterious, suspenseful",
            elements=[
                "Evidence or case file imagery",
                "Shadowy figures",
                "Red accent elements",
                "Case number or date",
            ],
        )
    
    async def _history_style(
        self,
        topic: str,
        audience: str,
    ) -> ThumbnailConcept:
        """Generate history documentary-style thumbnail."""
        return ThumbnailConcept(
            concept_description=f"Historical documentary style for {topic}",
            main_text=self._generate_main_text(topic, 4),
            secondary_text="HISTORY REVEALED",
            color_scheme="Sepia, aged paper tones",
            mood="Educational, historical",
            elements=[
                "Historical imagery or artifacts",
                "Vintage filter effect",
                "Timeline or map element",
                "Classical typography",
            ],
        )
    
    def _generate_main_text(self, topic: str, max_words: int = 4) -> str:
        """Generate main thumbnail text from topic.
        
        Args:
            topic: Video topic
            max_words: Maximum words in text
            
        Returns:
            Thumbnail text
        """
        words = topic.split()[:max_words]
        text = " ".join(words)
        if len(text) > 30:
            text = topic[:27] + "..."
        return text.upper()
    
    async def generate_prompt(self, concept: ThumbnailConcept) -> str:
        """Generate AI image generation prompt from concept.
        
        Args:
            concept: ThumbnailConcept object
            
        Returns:
            AI image generation prompt
        """
        prompt_parts = [
            f"YouTube thumbnail: {concept.concept_description}",
            f"Main text: '{concept.main_text}'",
            f"Mood: {concept.mood}",
            f"Color scheme: {concept.color_scheme}",
            f"Elements: {', '.join(concept.elements)}",
            "High quality, professional, eye-catching, 16:9 aspect ratio",
            "Trending on YouTube, high CTR design",
        ]
        
        if concept.secondary_text:
            prompt_parts.append(f"Secondary text: '{concept.secondary_text}'")
        
        return ", ".join(prompt_parts)
    
    def _estimate_ctr(self, concept: ThumbnailConcept) -> float:
        """Estimate CTR score for thumbnail concept.
        
        Args:
            concept: ThumbnailConcept object
            
        Returns:
            Estimated CTR score (0-1)
        """
        # Mock CTR estimation based on concept qualities
        base_score = 0.5
        
        # Bonus for clear text
        if len(concept.main_text) <= 20:
            base_score += 0.1
        
        # Bonus for defined elements
        if len(concept.elements) >= 4:
            base_score += 0.1
        
        # Bonus for specific mood
        if concept.mood:
            base_score += 0.05
        
        return min(1.0, base_score)
    
    def _fallback_thumbnail(self, topic: str) -> ThumbnailConcept:
        """Generate fallback thumbnail on error."""
        return ThumbnailConcept(
            concept_description=f"Thumbnail for {topic}",
            main_text=topic[:20].upper(),
            secondary_text="VIDEO",
            color_scheme="Blue gradient",
            mood="Professional",
            elements=["Title text", "Background image"],
            ctr_score=0.5,
            prompt=f"YouTube thumbnail for {topic}, professional design, high quality",
        )
    
    async def process(self, *args, **kwargs) -> ThumbnailConcept:
        """Process thumbnail generation request."""
        topic = kwargs.get("topic", "Untitled")
        format_type = kwargs.get("format_type", ContentFormat.EXPLAINER)
        audience = kwargs.get("target_audience", "general")
        return await self.generate(topic, format_type, audience)
