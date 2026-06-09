"""Script Templates for various content formats."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ScriptTemplate:
    """Script template structure."""
    
    format_name: str
    sections: Dict[str, str]
    guidelines: List[str]
    example_hooks: List[str]
    example_ctas: List[str]
    estimated_length_words: int


class ScriptTemplates:
    """Provides templates for different video script formats."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.templates = {
            "documentary": ScriptTemplate(
                format_name="documentary",
                sections={
                    "hook": "Start with a shocking revelation or compelling question about the subject",
                    "intro": "Set the scene, introduce the main subject/context",
                    "background": "Provide historical context and background information",
                    "development": "Develop the narrative with key events/facts",
                    "climax": "Present the most dramatic/revealing moment",
                    "resolution": "Show outcomes and consequences",
                    "conclusion": "Reflect on significance and lasting impact"
                },
                guidelines=[
                    "Use third-person narration",
                    "Include timestamps for archival footage",
                    "Build tension through pacing",
                    "Use expert interviews or quotes where possible",
                    "Create emotional connection to subjects"
                ],
                example_hooks=[
                    "In [year], something happened that would change everything...",
                    "This is the untold story of...",
                    "What you're about to see has never been revealed before..."
                ],
                example_ctas=[
                    "Subscribe for more deep dives into history's greatest stories",
                    "Share this documentary with someone who needs to hear it"
                ],
                estimated_length_words=1500
            ),
            
            "explainer": ScriptTemplate(
                format_name="explainer",
                sections={
                    "hook": "State the problem or question clearly",
                    "promise": "Tell viewers what they'll learn",
                    "explanation_part1": "Break down the concept into first principles",
                    "explanation_part2": "Build up with examples and applications",
                    "summary": "Recap the key points",
                    "next_steps": "Suggest how to apply the knowledge"
                },
                guidelines=[
                    "Use simple, accessible language",
                    "Include visual metaphors and analogies",
                    "Break complex ideas into digestible chunks",
                    "Use 'you' language to engage viewer",
                    "Include concrete examples"
                ],
                example_hooks=[
                    "Have you ever wondered how [thing] actually works?",
                    "Today I'm going to explain [topic] in just [time] minutes",
                    "Most people don't understand [concept] - here's the truth..."
                ],
                example_ctas=[
                    "Like this video if you learned something new",
                    "Comment below with what you'd like me to explain next"
                ],
                estimated_length_words=800
            ),
            
            "storytelling": ScriptTemplate(
                format_name="storytelling",
                sections={
                    "setup": "Introduce the character/situation",
                    "inciting_incident": "Present the challenge or opportunity",
                    "rising_action": "Build tension through obstacles",
                    "climax": "The decisive moment or turning point",
                    "falling_action": "Show immediate aftermath",
                    "resolution": "Reveal the lesson or transformation",
                    "reflection": "Connect story to viewer's life"
                },
                guidelines=[
                    "Use first or second person perspective",
                    "Include sensory details",
                    "Create emotional arc",
                    "Use dialogue where appropriate",
                    "End with clear takeaway"
                ],
                example_hooks=[
                    "Let me tell you about the time when...",
                    "I'll never forget the day that...",
                    "This story changed how I think about..."
                ],
                example_ctas=[
                    "Share your own story in the comments",
                    "Subscribe for more stories that matter"
                ],
                estimated_length_words=1000
            ),
            
            "review": ScriptTemplate(
                format_name="review",
                sections={
                    "hook": "State your overall verdict or rating upfront",
                    "intro": "Introduce the product/service being reviewed",
                    "pros": "Detail the strengths and positives",
                    "cons": "Address weaknesses and limitations",
                    "comparison": "Compare to alternatives if relevant",
                    "verdict": "Give final recommendation and who it's for"
                },
                guidelines=[
                    "Be honest and balanced",
                    "Include specific examples and evidence",
                    "Mention price and value proposition",
                    "Disclose any sponsorships or affiliations",
                    "Consider different user types"
                ],
                example_hooks=[
                    "After using [product] for [time], here's my honest review",
                    "Is [product] worth your money? Let's find out",
                    "I tested [product] so you don't have to..."
                ],
                example_ctas=[
                    "Check the links in description for best prices",
                    "Let me know if you agree with my review in the comments"
                ],
                estimated_length_words=900
            ),
            
            "news": ScriptTemplate(
                format_name="news",
                sections={
                    "headline": "Lead with the most important news",
                    "context": "Provide background and why it matters",
                    "details": "Share key facts and figures",
                    "implications": "Explain what this means going forward",
                    "wrap_up": "Summarize and tease future updates"
                },
                guidelines=[
                    "Lead with most important information",
                    "Keep sentences short and punchy",
                    "Cite sources clearly",
                    "Stay objective and factual",
                    "Update as new information emerges"
                ],
                example_hooks=[
                    "Breaking: [major news]",
                    "Just announced: [significant development]",
                    "You need to know about [important event]"
                ],
                example_ctas=[
                    "Subscribe for ongoing coverage of this story",
                    "Turn on notifications so you don't miss updates"
                ],
                estimated_length_words=400
            ),
            
            "tutorial": ScriptTemplate(
                format_name="tutorial",
                sections={
                    "hook": "Show the end result or what they'll achieve",
                    "requirements": "List what they need before starting",
                    "step_1": "First step with clear instructions",
                    "step_2": "Second step building on the first",
                    "step_3": "Continue with remaining steps",
                    "troubleshooting": "Address common issues",
                    "conclusion": "Recap and suggest next steps"
                },
                guidelines=[
                    "Number each step clearly",
                    "Show, don't just tell",
                    "Pause between steps for viewer to follow along",
                    "Anticipate common mistakes",
                    "Provide timestamps for each section"
                ],
                example_hooks=[
                    "By the end of this video, you'll be able to...",
                    "Follow these [number] steps to master [skill]",
                    "I'll show you exactly how to [achieve result]"
                ],
                example_ctas=[
                    "Download the worksheet in the description",
                    "Tag me when you try this technique"
                ],
                estimated_length_words=700
            )
        }
    
    def get_template(self, format_name: str) -> Optional[ScriptTemplate]:
        """Get template for a specific format."""
        return self.templates.get(format_name.lower())
    
    def get_all_formats(self) -> List[str]:
        """Get list of all available format templates."""
        return list(self.templates.keys())
    
    def generate_structure(self, format_name: str, topic: str) -> Dict:
        """Generate a structured outline for a script."""
        template = self.get_template(format_name)
        if not template:
            return {"error": f"No template found for {format_name}"}
        
        structure = {
            "topic": topic,
            "format": format_name,
            "estimated_word_count": template.estimated_length_words,
            "sections": {},
            "guidelines": template.guidelines
        }
        
        for section_name, description in template.sections.items():
            structure["sections"][section_name] = {
                "description": description,
                "content": ""  # To be filled by writer
            }
        
        return structure
    
    def get_hook_examples(self, format_name: str, count: int = 3) -> List[str]:
        """Get example hooks for a format."""
        template = self.get_template(format_name)
        if not template:
            return []
        return template.example_hooks[:count]
    
    def get_cta_examples(self, format_name: str, count: int = 3) -> List[str]:
        """Get example CTAs for a format."""
        template = self.get_template(format_name)
        if not template:
            return []
        return template.example_ctas[:count]
