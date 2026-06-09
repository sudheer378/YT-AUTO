"""SEO Engine - Generates SEO optimized content."""

from typing import List, Dict, Any, Optional
import logging

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import SEOData, ContentFormat


logger = get_logger(__name__)


class SEOEngine(BaseEngine):
    """Generates SEO-optimized titles, descriptions, tags, and keywords."""
    
    def __init__(self):
        super().__init__("seo_engine")
        self._categories = {
            "technology": "Science & Technology",
            "health": "Education",
            "business": "Education",
            "education": "Education",
            "entertainment": "Entertainment",
            "lifestyle": "Howto & Style",
            "science": "Education",
            "general": "People & Blogs",
        }
    
    async def generate(
        self,
        topic: str,
        description: str,
        niche: str = "general",
        format_type: ContentFormat = ContentFormat.EXPLAINER,
        target_keywords: Optional[List[str]] = None,
    ) -> SEOData:
        """Generate complete SEO data for a video.
        
        Args:
            topic: Video topic/title
            description: Brief description of content
            niche: Content niche
            format_type: Content format
            target_keywords: Optional list of target keywords
            
        Returns:
            SEOData object with all SEO elements
        """
        try:
            self.logger.info(f"Generating SEO data for: {topic}")
            
            # Generate title variations
            title = await self.generate_title(topic, format_type)
            
            # Generate description
            full_description = await self.generate_description(
                title, description, target_keywords or []
            )
            
            # Generate tags
            tags = await self.generate_tags(topic, niche, target_keywords or [])
            
            # Generate keywords
            keywords = target_keywords or await self.generate_keywords(topic, niche)
            
            # Determine category
            category = self._get_category(niche)
            
            return SEOData(
                title=title,
                description=full_description,
                tags=tags,
                keywords=keywords,
                category=category,
                language="en",
            )
            
        except Exception as e:
            self.logger.error(f"Error generating SEO data: {e}")
            return self._fallback_seo(topic, description, niche)
    
    async def generate_title(
        self,
        topic: str,
        format_type: ContentFormat,
    ) -> str:
        """Generate an optimized video title.
        
        Args:
            topic: Video topic
            format_type: Content format
            
        Returns:
            Optimized title
        """
        # TODO: Use AI to generate better titles
        format_prefixes = {
            ContentFormat.DOCUMENTARY: "The Complete Story:",
            ContentFormat.EXPLAINER: "Explained:",
            ContentFormat.STORYTELLING: "The Truth About:",
            ContentFormat.NEWS: "Breaking:",
            ContentFormat.SHORTS: "",
            ContentFormat.ANIMATION: "Animated Guide:",
            ContentFormat.MOTION_GRAPHICS: "Visual Guide:",
            ContentFormat.HYBRID: "",
            ContentFormat.CRIME_DOCUMENTARY: "Crime Files:",
            ContentFormat.HISTORY_DOCUMENTARY: "History Revealed:",
        }
        
        prefix = format_prefixes.get(format_type, "")
        if prefix:
            return f"{prefix} {topic}"
        return topic
    
    async def generate_description(
        self,
        title: str,
        base_description: str,
        keywords: List[str],
    ) -> str:
        """Generate an optimized video description.
        
        Args:
            title: Video title
            base_description: Base description text
            keywords: Target keywords
            
        Returns:
            Optimized description
        """
        # TODO: Use AI to generate better descriptions
        description_parts = [
            base_description,
            "",
            "📌 In this video:",
            f"- Deep dive into {title}",
            "- Key insights and analysis",
            "- Expert perspectives",
            "",
            "🔔 Subscribe for more content like this!",
            "",
            "#{}".format(" #".join(keywords[:5]) if keywords else "video"),
        ]
        return "\n".join(description_parts)
    
    async def generate_tags(
        self,
        topic: str,
        niche: str,
        keywords: List[str],
    ) -> List[str]:
        """Generate video tags.
        
        Args:
            topic: Video topic
            niche: Content niche
            keywords: Target keywords
            
        Returns:
            List of tags
        """
        tags = set()
        
        # Add topic-based tags
        topic_words = topic.lower().split()
        for word in topic_words:
            if len(word) > 3:
                tags.add(word)
        
        # Add keyword tags
        for kw in keywords:
            tags.add(kw.lower())
        
        # Add niche tags
        tags.add(niche.lower())
        tags.add(f"{niche} video")
        tags.add(f"{niche} content")
        
        # Add generic high-value tags
        tags.update(["tutorial", "guide", "explained", "2024"])
        
        return list(tags)[:20]  # YouTube limit is around 500 characters
    
    async def generate_keywords(
        self,
        topic: str,
        niche: str,
    ) -> List[str]:
        """Generate primary keywords.
        
        Args:
            topic: Video topic
            niche: Content niche
            
        Returns:
            List of keywords
        """
        # TODO: Use AI/keyword tools for better keyword generation
        keywords = [
            topic.lower(),
            f"{niche} {topic.lower()}",
            f"{topic.lower()} tutorial",
            f"{topic.lower()} guide",
            f"learn {topic.lower()}",
        ]
        return keywords[:10]
    
    def _get_category(self, niche: str) -> str:
        """Get YouTube category for niche.
        
        Args:
            niche: Content niche
            
        Returns:
            YouTube category name
        """
        return self._categories.get(niche.lower(), "People & Blogs")
    
    def _fallback_seo(
        self,
        topic: str,
        description: str,
        niche: str,
    ) -> SEOData:
        """Generate fallback SEO data on error.
        
        Args:
            topic: Video topic
            description: Base description
            niche: Content niche
            
        Returns:
            Fallback SEOData
        """
        return SEOData(
            title=topic,
            description=description,
            tags=[niche, "video", "content"],
            keywords=[topic.lower()],
            category=self._get_category(niche),
        )
    
    async def process(self, *args, **kwargs) -> SEOData:
        """Process SEO generation request."""
        topic = kwargs.get("topic", "Untitled")
        description = kwargs.get("description", "No description")
        niche = kwargs.get("niche", "general")
        format_type = kwargs.get("format_type", ContentFormat.EXPLAINER)
        target_keywords = kwargs.get("target_keywords")
        return await self.generate(topic, description, niche, format_type, target_keywords)
