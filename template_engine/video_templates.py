"""Video Templates for storyboarding and scene progression."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class VideoTemplate:
    """Video template with scene structure."""
    
    template_name: str
    scenes: List[Dict]
    total_estimated_seconds: int
    b_roll_suggestions: List[str]
    transition_notes: str


class VideoTemplates:
    """Provides templates for video structure and storyboarding."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.templates = {
            "standard_explainer": VideoTemplate(
                template_name="standard_explainer",
                scenes=[
                    {"time": "0:00-0:15", "type": "hook", "description": "Grab attention with bold statement"},
                    {"time": "0:15-0:30", "type": "intro", "description": "Introduce topic and what viewer will learn"},
                    {"time": "0:30-1:30", "type": "main_point_1", "description": "First key concept with examples"},
                    {"time": "1:30-2:30", "type": "main_point_2", "description": "Second key concept with visuals"},
                    {"time": "2:30-3:00", "type": "main_point_3", "description": "Third key concept or application"},
                    {"time": "3:00-3:30", "type": "summary", "description": "Recap main points"},
                    {"time": "3:30-4:00", "type": "cta", "description": "Call to action and outro"}
                ],
                total_estimated_seconds=240,
                b_roll_suggestions=[
                    "Screen recordings for tutorials",
                    "Stock footage for transitions",
                    "Text overlays for key points",
                    "Animated diagrams for concepts"
                ],
                transition_notes="Use smooth cuts between main points, add subtle zoom transitions"
            ),
            
            "documentary_style": VideoTemplate(
                template_name="documentary_style",
                scenes=[
                    {"time": "0:00-0:30", "type": "cold_open", "description": "Dramatic opening hook"},
                    {"time": "0:30-1:00", "type": "title_sequence", "description": "Title card with music"},
                    {"time": "1:00-3:00", "type": "setup", "description": "Establish context and background"},
                    {"time": "3:00-6:00", "type": "development", "description": "Main narrative development"},
                    {"time": "6:00-8:00", "type": "climax", "description": "Most dramatic/revealing moment"},
                    {"time": "8:00-9:00", "type": "resolution", "description": "Show outcomes"},
                    {"time": "9:00-10:00", "type": "conclusion", "description": "Final thoughts and CTA"}
                ],
                total_estimated_seconds=600,
                b_roll_suggestions=[
                    "Archival footage where relevant",
                    "Interview clips or quotes on screen",
                    "Cinematic B-roll for mood",
                    "Maps, timelines, and graphics"
                ],
                transition_notes="Slow fades, cross-dissolves for time transitions, dramatic pauses"
            ),
            
            "list_video": VideoTemplate(
                template_name="list_video",
                scenes=[
                    {"time": "0:00-0:20", "type": "hook", "description": "Tease the list and #1 item"},
                    {"time": "0:20-0:40", "type": "intro", "description": "Explain criteria and setup"},
                    {"time": "0:40-1:30", "type": "item_5", "description": "Fifth item with explanation"},
                    {"time": "1:30-2:20", "type": "item_4", "description": "Fourth item with visuals"},
                    {"time": "2:20-3:10", "type": "item_3", "description": "Third item - build anticipation"},
                    {"time": "3:10-4:00", "type": "item_2", "description": "Second item - near climax"},
                    {"time": "4:00-5:00", "type": "item_1", "description": "Top item - biggest reveal"},
                    {"time": "5:00-5:30", "type": "outro", "description": "Wrap up and CTA"}
                ],
                total_estimated_seconds=330,
                b_roll_suggestions=[
                    "Product shots or images for each item",
                    "Number graphics for countdown",
                    "Comparison charts if applicable",
                    "Reaction shots for emphasis"
                ],
                transition_notes="Consistent transition style between items, build energy toward #1"
            ),
            
            "storytelling": VideoTemplate(
                template_name="storytelling",
                scenes=[
                    {"time": "0:00-0:30", "type": "hook", "description": "Start in the middle of action"},
                    {"time": "0:30-1:00", "type": "backtrack", "description": "Flash back to beginning"},
                    {"time": "1:00-2:00", "type": "setup", "description": "Introduce characters/situation"},
                    {"time": "2:00-3:00", "type": "conflict", "description": "Present the challenge"},
                    {"time": "3:00-4:00", "type": "struggle", "description": "Show attempts and failures"},
                    {"time": "4:00-5:00", "type": "breakthrough", "description": "The turning point"},
                    {"time": "5:00-6:00", "type": "resolution", "description": "How it ended"},
                    {"time": "6:00-7:00", "type": "lesson", "description": "What was learned + CTA"}
                ],
                total_estimated_seconds=420,
                b_roll_suggestions=[
                    "Reenactment footage if possible",
                    "Emotional close-ups",
                    "Location shots",
                    "Symbolic imagery"
                ],
                transition_notes="Match cuts for emotional flow, use music to guide emotion"
            ),
            
            "tutorial_step_by_step": VideoTemplate(
                template_name="tutorial_step_by_step",
                scenes=[
                    {"time": "0:00-0:15", "type": "result_preview", "description": "Show finished result first"},
                    {"time": "0:15-0:30", "type": "requirements", "description": "List what's needed"},
                    {"time": "0:30-1:00", "type": "step_1", "description": "First step - slow and clear"},
                    {"time": "1:00-1:45", "type": "step_2", "description": "Second step building on first"},
                    {"time": "1:45-2:30", "type": "step_3", "description": "Third step with tips"},
                    {"time": "2:30-3:00", "type": "troubleshooting", "description": "Common mistakes to avoid"},
                    {"time": "3:00-3:30", "type": "final_result", "description": "Show completed work again"},
                    {"time": "3:30-4:00", "type": "next_steps", "description": "What to do next + CTA"}
                ],
                total_estimated_seconds=240,
                b_roll_suggestions=[
                    "Close-up shots of hands/work",
                    "Screen recording for digital tutorials",
                    "Before/after comparisons",
                    "Text callouts for important details"
                ],
                transition_notes="Clean cuts, pause briefly after each step, use progress indicator"
            ),
            
            "news_update": VideoTemplate(
                template_name="news_update",
                scenes=[
                    {"time": "0:00-0:10", "type": "headline", "description": "Lead story immediately"},
                    {"time": "0:10-0:30", "type": "context", "description": "Why this matters now"},
                    {"time": "0:30-1:00", "type": "details", "description": "Key facts and figures"},
                    {"time": "1:00-1:30", "type": "analysis", "description": "What it means"},
                    {"time": "1:30-1:50", "type": "additional_stories", "description": "Quick other news"},
                    {"time": "1:50-2:00", "type": "wrap_up", "description": "What to watch for + CTA"}
                ],
                total_estimated_seconds=120,
                b_roll_suggestions=[
                    "News footage and clips",
                    "Headline graphics",
                    "Lower thirds for names/titles",
                    "Timeline graphics"
                ],
                transition_notes="Quick cuts, energetic pacing, urgency in transitions"
            )
        }
    
    def get_template(self, template_name: str) -> Optional[VideoTemplate]:
        """Get a specific video template."""
        return self.templates.get(template_name.lower())
    
    def recommend_template(self, content_type: str, desired_length: int = 300) -> VideoTemplate:
        """Recommend best video template based on content type and length."""
        content_lower = content_type.lower()
        
        # Match by content type
        if "documentary" in content_lower or "deep dive" in content_lower:
            return self.templates["documentary_style"]
        elif "list" in content_lower or "top " in content_lower:
            return self.templates["list_video"]
        elif "story" in content_lower or "narrative" in content_lower:
            return self.templates["storytelling"]
        elif "tutorial" in content_lower or "how to" in content_lower:
            return self.templates["tutorial_step_by_step"]
        elif "news" in content_lower or "update" in content_lower:
            return self.templates["news_update"]
        else:
            # Default based on length
            if desired_length > 400:
                return self.templates["documentary_style"]
            elif desired_length > 200:
                return self.templates["standard_explainer"]
            else:
                return self.templates["news_update"]
    
    def get_all_templates(self) -> List[str]:
        """Get list of all available templates."""
        return list(self.templates.keys())
    
    def generate_shot_list(self, template_name: str) -> List[Dict]:
        """Generate a shot list from template."""
        template = self.get_template(template_name)
        if not template:
            return []
        
        shot_list = []
        for scene in template.scenes:
            shot_list.append({
                "scene": scene["type"],
                "time": scene["time"],
                "description": scene["description"],
                "shots_needed": ["A-roll (talking head)", "B-roll support", "Graphics/overlay"],
                "notes": ""
            })
        
        return shot_list
