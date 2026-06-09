"""Thumbnail Templates for high-CTR visual design."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThumbnailTemplate:
    """Thumbnail template structure."""
    
    template_name: str
    description: str
    best_for: List[str]
    elements: Dict[str, str]
    color_scheme: List[str]
    text_guidelines: List[str]
    composition_notes: str


class ThumbnailTemplates:
    """Provides templates for thumbnail design."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.templates = {
            "face_reaction": ThumbnailTemplate(
                template_name="face_reaction",
                description="Large face with strong emotional expression",
                best_for=["reaction videos", "shocking content", "personal stories", "vlogs"],
                elements={
                    "primary": "Face with clear emotion (surprise, shock, excitement)",
                    "secondary": "Relevant object or background element",
                    "text": "3-5 word curiosity trigger"
                },
                color_scheme=["high contrast", "saturated colors", "warm tones"],
                text_guidelines=[
                    "Use bold, thick fonts",
                    "Maximum 5 words",
                    "Place text opposite the face",
                    "Add outline/shadow for readability"
                ],
                composition_notes="Rule of thirds - face on left or right third, looking toward center"
            ),
            
            "before_after": ThumbnailTemplate(
                template_name="before_after",
                description="Split screen showing transformation",
                best_for=["tutorials", "makeovers", "progress videos", "comparisons"],
                elements={
                    "left": "Before state with label",
                    "right": "After state with label", 
                    "center": "Arrow or dividing line"
                },
                color_scheme=["contrasting sides", "green for after", "muted for before"],
                text_guidelines=[
                    "Label each side clearly",
                    "Use 'BEFORE' and 'AFTER' or similar",
                    "Keep text minimal on image itself"
                ],
                composition_notes="Clean split down the middle, ensure both sides are equally visible"
            ),
            
            "mystery_box": ThumbnailTemplate(
                template_name="mystery_box",
                description="Obscured or hidden element creating curiosity",
                best_for=["unboxing", "reveals", "announcements", "teasers"],
                elements={
                    "primary": "Mysterious object or blurred element",
                    "secondary": "Question mark or '???' overlay",
                    "text": "Curiosity-driven question"
                },
                color_scheme=["dark background", "spotlight effect", "mystery colors"],
                text_guidelines=[
                    "Ask a question",
                    "Use words like 'SECRET', 'REVEALED', 'FINALLY'",
                    "Create information gap"
                ],
                composition_notes="Central focus with darkness/vignette around edges"
            ),
            
            "list_number": ThumbnailTemplate(
                template_name="list_number",
                description="Large number indicating list quantity",
                best_for=["top 10 lists", "tips videos", "countdowns", "rankings"],
                elements={
                    "primary": "Large bold number",
                    "secondary": "Representative images of items",
                    "text": "Topic description"
                },
                color_scheme=["bold number color", "contrasting background"],
                text_guidelines=[
                    "Make number HUGE",
                    "Number should be first thing viewers see",
                    "Brief topic description below number"
                ],
                composition_notes="Number takes up 40-50% of thumbnail space"
            ),
            
            "comparison": ThumbnailTemplate(
                template_name="comparison",
                description="Two products/options side by side",
                best_for=["product comparisons", "versus videos", "buying guides"],
                elements={
                    "left": "Product/option A",
                    "right": "Product/option B",
                    "center": "VS text or dividing element"
                },
                color_scheme=["brand colors for each", "neutral background"],
                text_guidelines=[
                    "Include product names if short",
                    "Use 'VS' or 'COMPARE'",
                    "Add winner indicator if appropriate"
                ],
                composition_notes="Equal weight to both sides, clear separation"
            ),
            
            "minimal_text": ThumbnailTemplate(
                template_name="minimal_text",
                description="Clean design with minimal text overlay",
                best_for=["professional content", "tech reviews", "educational"],
                elements={
                    "primary": "High-quality hero image",
                    "secondary": "Subtle branding element",
                    "text": "2-3 word key phrase"
                },
                color_scheme=["clean", "professional", "brand-aligned"],
                text_guidelines=[
                    "Less is more",
                    "Let image speak for itself",
                    "Use elegant typography"
                ],
                composition_notes="Professional photography, clean edges, plenty of negative space"
            ),
            
            "shock_factor": ThumbnailTemplate(
                template_name="shock_factor",
                description="Bold, attention-grabbing visual",
                best_for=["controversial topics", "dramatic reveals", "investigations"],
                elements={
                    "primary": "Dramatic visual or expression",
                    "secondary": "Bold text overlay",
                    "accent": "Red arrows, circles, or highlights"
                },
                color_scheme=["high saturation", "red accents", "dramatic lighting"],
                text_guidelines=[
                    "Use power words: SHOCKING, EXPOSED, TRUTH",
                    "All caps for impact",
                    "Exclamation points acceptable"
                ],
                composition_notes="Maximum visual impact, don't be subtle"
            )
        }
    
    def get_template(self, template_name: str) -> Optional[ThumbnailTemplate]:
        """Get a specific thumbnail template."""
        return self.templates.get(template_name.lower())
    
    def recommend_template(self, content_type: str, niche: str = "general") -> ThumbnailTemplate:
        """Recommend best thumbnail template for content type."""
        content_lower = content_type.lower()
        
        # Mapping logic
        if any(word in content_lower for word in ["reaction", "vlog", "personal"]):
            return self.templates["face_reaction"]
        elif any(word in content_lower for word in ["tutorial", "transformation", "progress"]):
            return self.templates["before_after"]
        elif any(word in content_lower for word in ["unboxing", "reveal", "announcement"]):
            return self.templates["mystery_box"]
        elif any(word in content_lower for word in ["top ", "list", "tips", "ways"]):
            return self.templates["list_number"]
        elif any(word in content_lower for word in ["vs", "versus", "compare", "comparison"]):
            return self.templates["comparison"]
        elif any(word in content_lower for word in ["professional", "tech", "review"]):
            return self.templates["minimal_text"]
        else:
            return self.templates["face_reaction"]  # Default
    
    def get_all_templates(self) -> List[str]:
        """Get list of all available templates."""
        return list(self.templates.keys())
    
    def generate_prompt(self, template_name: str, topic: str) -> str:
        """Generate an AI image generation prompt for thumbnail."""
        template = self.get_template(template_name)
        if not template:
            return ""
        
        prompt_parts = [
            f"YouTube thumbnail, {template.description}",
            f"Topic: {topic}",
            f"Style: {', '.join(template.color_scheme)}",
            f"Composition: {template.composition_notes}"
        ]
        
        return ". ".join(prompt_parts)
