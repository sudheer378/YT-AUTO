"""Retention Prediction Engine for YouTube content."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class RetentionAnalysis:
    """Retention analysis result."""
    
    predicted_retention: float  # Percentage (0-100)
    hook_score: float
    pacing_score: float
    engagement_score: float
    structure_score: float
    estimated_avg_view_duration: float  # in seconds
    factors: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    drop_off_points: List[str] = field(default_factory=list)
    confidence: float = 0.80


class RetentionPredictor:
    """Predicts audience retention for video content."""
    
    def __init__(self):
        self.hook_patterns = {
            "question_opening": 0.15,
            "shocking_statement": 0.20,
            "story_beginning": 0.15,
            "promise_of_value": 0.20,
            "visual_hook": 0.15,
            "curiosity_gap": 0.15,
        }
        
        self.retention_triggers = [
            "pattern_interrupt",
            "open_loop",
            "cliffhanger",
            "reveal",
            "call_to_action",
            "story_progression"
        ]
    
    def predict(
        self,
        script: str,
        video_length_seconds: int = 600,
        format_type: str = "explainer",
        niche: str = "general"
    ) -> RetentionAnalysis:
        """
        Predict retention based on script analysis.
        
        Args:
            script: Full video script
            video_length_seconds: Expected video length
            format_type: Video format (documentary, explainer, etc.)
            niche: Content niche
            
        Returns:
            RetentionAnalysis with predicted retention and breakdown
        """
        logger.info(f"Predicting retention for {video_length_seconds}s {format_type} video")
        
        # Analyze components
        hook_analysis = self._analyze_hook(script)
        pacing_analysis = self._analyze_pacing(script, video_length_seconds)
        engagement_analysis = self._analyze_engagement(script)
        structure_analysis = self._analyze_structure(script, format_type)
        
        # Calculate component scores
        hook_score = sum(hook_analysis.values()) / len(hook_analysis) * 100
        pacing_score = sum(pacing_analysis.values()) / len(pacing_analysis) * 100
        engagement_score = sum(engagement_analysis.values()) / len(engagement_analysis) * 100
        structure_score = sum(structure_analysis.values()) / len(structure_analysis) * 100
        
        # Weighted retention prediction
        # Hook is critical (first 30 seconds determine 70% of retention)
        predicted_retention = (
            hook_score * 0.35 +
            pacing_score * 0.25 +
            engagement_score * 0.25 +
            structure_score * 0.15
        )
        
        # Adjust for video length (shorter videos tend to have higher % retention)
        length_factor = 1.0
        if video_length_seconds > 600:
            length_factor = 0.9
        elif video_length_seconds > 900:
            length_factor = 0.85
        elif video_length_seconds < 300:
            length_factor = 1.1
        
        predicted_retention *= length_factor
        
        # Clamp to realistic range
        predicted_retention = max(20.0, min(85.0, predicted_retention))
        
        # Estimate average view duration
        estimated_avd = (predicted_retention / 100) * video_length_seconds
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            hook_analysis,
            pacing_analysis,
            engagement_analysis,
            structure_analysis,
            script
        )
        
        # Identify potential drop-off points
        drop_off_points = self._identify_drop_off_points(script, format_type)
        
        # Compile factors
        factors = {
            **{f"hook_{k}": v for k, v in hook_analysis.items()},
            **{f"pacing_{k}": v for k, v in pacing_analysis.items()},
            **{f"engagement_{k}": v for k, v in engagement_analysis.items()},
            **{f"structure_{k}": v for k, v in structure_analysis.items()},
        }
        
        return RetentionAnalysis(
            predicted_retention=round(predicted_retention, 2),
            hook_score=round(hook_score, 2),
            pacing_score=round(pacing_score, 2),
            engagement_score=round(engagement_score, 2),
            structure_score=round(structure_score, 2),
            estimated_avg_view_duration=round(estimated_avd, 0),
            factors=factors,
            recommendations=recommendations,
            drop_off_points=drop_off_points,
            confidence=0.80
        )
    
    def _analyze_hook(self, script: str) -> Dict[str, float]:
        """Analyze the hook (first 50-100 words) of the script."""
        analysis = {
            "question_opening": 0.5,
            "shocking_statement": 0.5,
            "story_beginning": 0.5,
            "promise_of_value": 0.5,
            "visual_hook": 0.5,
            "curiosity_gap": 0.5,
        }
        
        # Get first 100 words as hook
        words = script.split()[:100]
        hook_text = " ".join(words).lower()
        
        # Question opening
        if "?" in hook_text or hook_text.startswith(("how", "why", "what", "when", "where", "have you")):
            analysis["question_opening"] = 0.9
        
        # Shocking statement
        shocking_words = ["shocking", "incredible", "unbelievable", "never", "nobody", "secret", "truth"]
        if any(word in hook_text for word in shocking_words):
            analysis["shocking_statement"] = 0.85
        
        # Story beginning
        story_indicators = ["once", "it all started", "picture this", "imagine", "let me tell you"]
        if any(indicator in hook_text for indicator in story_indicators):
            analysis["story_beginning"] = 0.85
        
        # Promise of value
        value_words = ["you'll learn", "by the end", "we'll cover", "i'll show", "discover"]
        if any(word in hook_text for word in value_words):
            analysis["promise_of_value"] = 0.85
        
        # Visual hook (descriptive language)
        visual_words = ["look", "see", "watch", "imagine", "picture", "visualize"]
        if any(word in hook_text for word in visual_words):
            analysis["visual_hook"] = 0.8
        
        # Curiosity gap
        curiosity_phrases = ["but here's", "however", "what most", "the real", "actually"]
        if any(phrase in hook_text for phrase in curiosity_phrases):
            analysis["curiosity_gap"] = 0.85
        
        return analysis
    
    def _analyze_pacing(self, script: str, video_length: int) -> Dict[str, float]:
        """Analyze pacing throughout the script."""
        analysis = {
            "word_rate_optimal": 0.5,
            "sentence_variation": 0.5,
            "paragraph_breaks": 0.5,
            "information_density": 0.5,
        }
        
        words = script.split()
        total_words = len(words)
        
        # Word rate (words per minute)
        wpm = (total_words / video_length) * 60
        if 140 <= wpm <= 160:
            analysis["word_rate_optimal"] = 1.0
        elif 120 <= wpm <= 180:
            analysis["word_rate_optimal"] = 0.7
        else:
            analysis["word_rate_optimal"] = 0.5
        
        # Sentence variation
        sentences = script.replace("!", ".").replace("?", ".").split(".")
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        if sentence_lengths:
            avg_len = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((l - avg_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            if 10 <= variance <= 50:
                analysis["sentence_variation"] = 0.9
            elif 5 <= variance <= 70:
                analysis["sentence_variation"] = 0.7
            else:
                analysis["sentence_variation"] = 0.5
        
        # Paragraph breaks (section markers)
        paragraphs = [p.strip() for p in script.split("\n\n") if p.strip()]
        if len(paragraphs) >= 5:
            analysis["paragraph_breaks"] = 0.9
        elif len(paragraphs) >= 3:
            analysis["paragraph_breaks"] = 0.7
        else:
            analysis["paragraph_breaks"] = 0.5
        
        # Information density (technical terms ratio)
        technical_indicators = ["therefore", "thus", "consequently", "specifically", "technically"]
        tech_count = sum(1 for word in technical_indicators if word in script.lower())
        density = tech_count / max(1, total_words) * 100
        if density < 2:
            analysis["information_density"] = 0.9
        elif density < 5:
            analysis["information_density"] = 0.7
        else:
            analysis["information_density"] = 0.5
        
        return analysis
    
    def _analyze_engagement(self, script: str) -> Dict[str, float]:
        """Analyze engagement elements in the script."""
        analysis = {
            "direct_address": 0.5,
            "storytelling_elements": 0.5,
            "emotional_language": 0.5,
            "interactive_elements": 0.5,
        }
        
        script_lower = script.lower()
        
        # Direct address (you/your)
        you_count = script_lower.count(" you ") + script_lower.count(" your ")
        if you_count > 10:
            analysis["direct_address"] = 0.9
        elif you_count > 5:
            analysis["direct_address"] = 0.7
        
        # Storytelling elements
        story_words = ["story", "journey", "adventure", "challenge", "overcome", "struggle"]
        if any(word in script_lower for word in story_words):
            analysis["storytelling_elements"] = 0.85
        
        # Emotional language
        emotion_words = ["amazing", "incredible", "frustrating", "exciting", "terrifying", "beautiful"]
        emotion_count = sum(1 for word in emotion_words if word in script_lower)
        if emotion_count > 5:
            analysis["emotional_language"] = 0.9
        elif emotion_count > 2:
            analysis["emotional_language"] = 0.7
        
        # Interactive elements
        interactive_phrases = ["let me know", "comment below", "what do you think", "pause here"]
        if any(phrase in script_lower for phrase in interactive_phrases):
            analysis["interactive_elements"] = 0.85
        
        return analysis
    
    def _analyze_structure(self, script: str, format_type: str) -> Dict[str, float]:
        """Analyze overall script structure."""
        analysis = {
            "clear_intro": 0.5,
            "logical_flow": 0.5,
            "transitions": 0.5,
            "strong_conclusion": 0.5,
        }
        
        script_lower = script.lower()
        lines = script_lower.split("\n")
        
        # Clear intro
        intro_markers = ["intro", "introduction", "welcome", "today we", "in this video"]
        if any(marker in script_lower[:500] for marker in intro_markers):
            analysis["clear_intro"] = 0.9
        
        # Logical flow (section headers or clear progression)
        section_markers = ["first", "second", "third", "next", "then", "finally", "conclusion"]
        marker_count = sum(1 for marker in section_markers if marker in script_lower)
        if marker_count >= 4:
            analysis["logical_flow"] = 0.9
        elif marker_count >= 2:
            analysis["logical_flow"] = 0.7
        
        # Transitions
        transition_words = ["however", "therefore", "meanwhile", "moreover", "consequently", "now"]
        transition_count = sum(1 for word in transition_words if word in script_lower)
        if transition_count >= 5:
            analysis["transitions"] = 0.9
        elif transition_count >= 2:
            analysis["transitions"] = 0.7
        
        # Strong conclusion
        conclusion_markers = ["conclusion", "to summarize", "in summary", "thanks for watching", "subscribe"]
        if any(marker in script_lower[-500:] for marker in conclusion_markers):
            analysis["strong_conclusion"] = 0.9
        
        return analysis
    
    def _generate_recommendations(
        self,
        hook_analysis: Dict[str, float],
        pacing_analysis: Dict[str, float],
        engagement_analysis: Dict[str, float],
        structure_analysis: Dict[str, float],
        script: str
    ) -> List[str]:
        """Generate recommendations to improve retention."""
        recommendations = []
        
        # Hook recommendations
        if hook_analysis.get("question_opening", 0.5) < 0.7:
            recommendations.append(
                "Start with a compelling question to immediately engage viewers"
            )
        
        if hook_analysis.get("curiosity_gap", 0.5) < 0.7:
            recommendations.append(
                "Create a curiosity gap in the first 10 seconds - tease what's coming"
            )
        
        # Pacing recommendations
        if pacing_analysis.get("sentence_variation", 0.5) < 0.7:
            recommendations.append(
                "Vary sentence length - mix short punchy sentences with longer explanations"
            )
        
        if pacing_analysis.get("paragraph_breaks", 0.5) < 0.7:
            recommendations.append(
                "Add more section breaks to create natural pause points"
            )
        
        # Engagement recommendations
        if engagement_analysis.get("direct_address", 0.5) < 0.7:
            recommendations.append(
                "Use 'you' and 'your' more frequently to speak directly to viewers"
            )
        
        if engagement_analysis.get("storytelling_elements", 0.5) < 0.7:
            recommendations.append(
                "Incorporate storytelling elements - challenges, journeys, transformations"
            )
        
        # Structure recommendations
        if structure_analysis.get("transitions", 0.5) < 0.7:
            recommendations.append(
                "Add clearer transitions between sections to maintain flow"
            )
        
        return recommendations[:6]
    
    def _identify_drop_off_points(self, script: str, format_type: str) -> List[str]:
        """Identify potential drop-off points in the video."""
        drop_offs = []
        
        # Common drop-off zones
        drop_offs.append("0:00-0:30 - Critical hook period - 70% of viewers decide to stay")
        
        words = script.split()
        third_point = len(words) // 3
        two_thirds = (len(words) // 3) * 2
        
        drop_offs.append(
            f"~{third_point // 25}s - First major content transition point"
        )
        drop_offs.append(
            f"~{two_thirds // 25}s - Mid-video fatigue zone - add pattern interrupt"
        )
        
        return drop_offs
