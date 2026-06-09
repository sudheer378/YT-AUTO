"""Script Engine - Generates video scripts."""

from typing import List, Dict, Any, Optional
import logging

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import Script, ScriptSection, ContentFormat


logger = get_logger(__name__)


class ScriptEngine(BaseEngine):
    """Generates complete video scripts with hooks, intros, body, and CTAs."""
    
    def __init__(self):
        super().__init__("script_engine")
        self._format_structures = {
            ContentFormat.DOCUMENTARY: self._documentary_structure,
            ContentFormat.EXPLAINER: self._explainer_structure,
            ContentFormat.STORYTELLING: self._storytelling_structure,
            ContentFormat.NEWS: self._news_structure,
            ContentFormat.SHORTS: self._shorts_structure,
            ContentFormat.ANIMATION: self._explainer_structure,
            ContentFormat.MOTION_GRAPHICS: self._explainer_structure,
            ContentFormat.HYBRID: self._hybrid_structure,
            ContentFormat.CRIME_DOCUMENTARY: self._crime_structure,
            ContentFormat.HISTORY_DOCUMENTARY: self._history_structure,
        }
    
    async def generate(
        self,
        topic: str,
        description: str,
        format_type: ContentFormat = ContentFormat.EXPLAINER,
        target_duration_seconds: int = 600,
        tone: str = "professional",
    ) -> Script:
        """Generate a complete video script.
        
        Args:
            topic: Video topic
            description: Brief description
            format_type: Content format
            target_duration_seconds: Target duration in seconds
            tone: Script tone
            
        Returns:
            Complete Script object
        """
        try:
            self.logger.info(f"Generating {format_type.value} script for: {topic}")
            
            # Get structure for format
            structure_fn = self._format_structures.get(
                format_type, self._explainer_structure
            )
            
            sections = await structure_fn(topic, description, target_duration_seconds, tone)
            
            # Calculate total duration and word count
            total_duration = sum(s.duration_seconds for s in sections)
            word_count = sum(len(s.content.split()) for s in sections)
            
            return Script(
                title=topic,
                topic=topic,
                format=format_type,
                sections=sections,
                total_duration_seconds=total_duration,
                word_count=word_count,
                notes=f"Generated for {tone} tone",
            )
            
        except Exception as e:
            self.logger.error(f"Error generating script: {e}")
            return self._fallback_script(topic, description, format_type)
    
    async def _documentary_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate documentary-style script structure."""
        hook_duration = min(45, duration // 10)
        intro_duration = min(90, duration // 6)
        body_duration = duration - hook_duration - intro_duration - 60
        cta_duration = 60
        
        return [
            ScriptSection(
                section_type="hook",
                content=f"[DRAMATIC OPENING] What if everything you knew about {topic} was wrong? In this documentary, we uncover the hidden truth...",
                duration_seconds=hook_duration,
                visual_cues=["Dramatic B-roll", "Tension-building music", "Quick cuts"],
            ),
            ScriptSection(
                section_type="intro",
                content=f"Welcome to our deep dive into {topic}. {description} Today, we'll explore the history, the key players, and the impact on our world.",
                duration_seconds=intro_duration,
                visual_cues=["Host on camera", "Title sequence", "Establishing shots"],
            ),
            ScriptSection(
                section_type="body",
                content=f"[MAIN CONTENT] The story of {topic} begins... [Detailed exploration with expert interviews, data, and analysis]",
                duration_seconds=body_duration,
                visual_cues=["Interviews", "Archival footage", "Graphics", "B-roll"],
            ),
            ScriptSection(
                section_type="cta",
                content="If you found this documentary insightful, please like, subscribe, and hit the notification bell. What topic should we cover next? Let us know in the comments.",
                duration_seconds=cta_duration,
                visual_cues=["End screen", "Subscribe animation", "Comment prompt"],
            ),
        ]
    
    async def _explainer_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate explainer-style script structure."""
        hook_duration = min(30, duration // 8)
        intro_duration = min(60, duration // 5)
        body_duration = duration - hook_duration - intro_duration - 45
        cta_duration = 45
        
        return [
            ScriptSection(
                section_type="hook",
                content=f"Ever wondered how {topic} actually works? In the next few minutes, we'll break it down step by step.",
                duration_seconds=hook_duration,
                visual_cues=["Animated intro", "Question on screen", "Engaging visuals"],
            ),
            ScriptSection(
                section_type="intro",
                content=f"Hi everyone! Today we're exploring {topic}. {description} By the end of this video, you'll understand exactly how it all fits together.",
                duration_seconds=intro_duration,
                visual_cues=["Host introduction", "Topic overview graphic"],
            ),
            ScriptSection(
                section_type="body",
                content=f"Let's start with the basics. [Point 1]... [Point 2]... [Point 3]... Now, here's where it gets interesting...",
                duration_seconds=body_duration,
                visual_cues=["Diagrams", "Screen captures", "Examples", "Comparisons"],
            ),
            ScriptSection(
                section_type="cta",
                content="Hope this helped clarify {topic}! Drop a like if you learned something, subscribe for more explainers, and comment below with your questions.",
                duration_seconds=cta_duration,
                visual_cues=["Summary graphic", "Subscribe button", "Comment section highlight"],
            ),
        ]
    
    async def _storytelling_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate storytelling-style script structure."""
        hook_duration = min(45, duration // 8)
        intro_duration = min(90, duration // 6)
        body_duration = duration - hook_duration - intro_duration - 60
        cta_duration = 60
        
        return [
            ScriptSection(
                section_type="hook",
                content=f"This is the story of {topic}. A story that will change how you see everything...",
                duration_seconds=hook_duration,
                visual_cues=["Cinematic opening", "Emotional music", "Character introduction"],
            ),
            ScriptSection(
                section_type="intro",
                content=f"Every great story has a beginning. Ours starts with {description}. Let me take you back to when it all began...",
                duration_seconds=intro_duration,
                visual_cues=["Narrative setup", "Context visuals", "Character/subject intro"],
            ),
            ScriptSection(
                section_type="body",
                content=f"And then, everything changed. [The journey unfolds with challenges, discoveries, and transformations]...",
                duration_seconds=body_duration,
                visual_cues=["Story progression", "Conflict visuals", "Resolution buildup"],
            ),
            ScriptSection(
                section_type="cta",
                content="What did you think of this story? Share your thoughts below, and don't forget to subscribe for more narratives that matter.",
                duration_seconds=cta_duration,
                visual_cues=["Reflection moment", "Call to action", "Next story teaser"],
            ),
        ]
    
    async def _news_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate news-style script structure."""
        return [
            ScriptSection(
                section_type="hook",
                content=f"BREAKING: Major developments in {topic}. Here's what you need to know right now.",
                duration_seconds=20,
                visual_cues=["Breaking news graphic", "Urgent music"],
            ),
            ScriptSection(
                section_type="intro",
                content=f"Good day, I'm your host. Today's top story: {description}",
                duration_seconds=30,
                visual_cues=["News desk", "Lower thirds"],
            ),
            ScriptSection(
                section_type="body",
                content=f"[Details of the story with facts, quotes, and context]...",
                duration_seconds=duration - 80,
                visual_cues=["Footage", "Expert clips", "Data graphics"],
            ),
            ScriptSection(
                section_type="cta",
                content="Stay tuned for updates. Subscribe for breaking news coverage.",
                duration_seconds=30,
                visual_cues=["Outro graphic", "Social media handles"],
            ),
        ]
    
    async def _shorts_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate Shorts-style script structure (under 60 seconds)."""
        actual_duration = min(duration, 55)
        return [
            ScriptSection(
                section_type="hook",
                content=f"Wait until you hear this about {topic}!",
                duration_seconds=5,
                visual_cues=["Quick cut", "Text overlay"],
            ),
            ScriptSection(
                section_type="body",
                content=f"{description} Here's the key point you need to know...",
                duration_seconds=actual_duration - 15,
                visual_cues=["Fast-paced visuals", "Key points on screen"],
            ),
            ScriptSection(
                section_type="cta",
                content="Follow for more! Comment your thoughts!",
                duration_seconds=10,
                visual_cues=["Subscribe animation", "Loop setup"],
            ),
        ]
    
    async def _hybrid_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate hybrid-style script structure."""
        return await self._explainer_structure(topic, description, duration, tone)
    
    async def _crime_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate crime documentary structure."""
        return await self._documentary_structure(topic, description, duration, "dramatic")
    
    async def _history_structure(
        self,
        topic: str,
        description: str,
        duration: int,
        tone: str,
    ) -> List[ScriptSection]:
        """Generate history documentary structure."""
        return await self._documentary_structure(topic, description, duration, "educational")
    
    def _fallback_script(
        self,
        topic: str,
        description: str,
        format_type: ContentFormat,
    ) -> Script:
        """Generate fallback script on error."""
        return Script(
            title=topic,
            topic=topic,
            format=format_type,
            sections=[
                ScriptSection(
                    section_type="hook",
                    content=f"Introduction to {topic}",
                    duration_seconds=30,
                ),
                ScriptSection(
                    section_type="body",
                    content=description,
                    duration_seconds=300,
                ),
                ScriptSection(
                    section_type="cta",
                    content="Thank you for watching!",
                    duration_seconds=30,
                ),
            ],
            total_duration_seconds=360,
            word_count=len(description.split()),
        )
    
    async def process(self, *args, **kwargs) -> Script:
        """Process script generation request."""
        topic = kwargs.get("topic", "Untitled")
        description = kwargs.get("description", "No description")
        format_type = kwargs.get("format_type", ContentFormat.EXPLAINER)
        duration = kwargs.get("target_duration_seconds", 600)
        tone = kwargs.get("tone", "professional")
        return await self.generate(topic, description, format_type, duration, tone)
