"""Format Selector for recommending optimal content formats."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class FormatRecommendation:
    """Format recommendation result."""
    
    recommended_format: str
    confidence: float  # 0-100
    alternative_formats: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)
    format_details: Dict = field(default_factory=dict)


class FormatSelector:
    """Selects optimal content format based on topic and audience."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Format characteristics
        self.formats = {
            "documentary": {
                "best_for": ["deep dives", "history", "biography", "investigation", "true crime"],
                "length_range": (600, 1800),
                "complexity": "high",
                "research_required": "extensive",
                "audience": "engaged learners"
            },
            "explainer": {
                "best_for": ["how to", "tutorial", "concept explanation", "beginner guide"],
                "length_range": (300, 600),
                "complexity": "medium",
                "research_required": "moderate",
                "audience": "general"
            },
            "storytelling": {
                "best_for": ["personal story", "case study", "narrative", "journey"],
                "length_range": (400, 900),
                "complexity": "medium",
                "research_required": "moderate",
                "audience": "emotionally engaged"
            },
            "news": {
                "best_for": ["current events", "breaking news", "updates", "announcements"],
                "length_range": (180, 400),
                "complexity": "low",
                "research_required": "minimal",
                "audience": "time-sensitive viewers"
            },
            "review": {
                "best_for": ["product review", "comparison", "testing", "opinion"],
                "length_range": (400, 800),
                "complexity": "medium",
                "research_required": "moderate",
                "audience": "buyers/researchers"
            },
            "animation": {
                "best_for": ["abstract concepts", "visual stories", "entertainment", "metaphors"],
                "length_range": (300, 600),
                "complexity": "high",
                "research_required": "moderate",
                "audience": "visual learners"
            },
            "shorts": {
                "best_for": ["quick tips", "highlights", "teasers", "viral content"],
                "length_range": (15, 60),
                "complexity": "low",
                "research_required": "minimal",
                "audience": "mobile/scrollers"
            },
            "hybrid": {
                "best_for": ["multi-format", "variety", "experimental"],
                "length_range": (400, 900),
                "complexity": "variable",
                "research_required": "variable",
                "audience": "diverse"
            }
        }
    
    def recommend(
        self,
        topic: str,
        niche: str = "general",
        target_audience: str = "general",
        desired_length_seconds: int = 0,
        production_capacity: str = "medium"
    ) -> FormatRecommendation:
        """
        Recommend optimal format for content.
        
        Args:
            topic: Content topic/title
            niche: Content niche
            target_audience: Primary audience type
            desired_length_seconds: Desired video length
            production_capacity: Production capability (low/medium/high)
            
        Returns:
            FormatRecommendation with best format and reasoning
        """
        logger.info(f"Recommending format for topic: {topic[:50]}...")
        
        topic_lower = topic.lower()
        
        # Score each format
        format_scores = {}
        for format_name, format_info in self.formats.items():
            score = self._score_format(
                format_name,
                format_info,
                topic_lower,
                niche.lower(),
                target_audience.lower(),
                desired_length_seconds,
                production_capacity
            )
            format_scores[format_name] = score
        
        # Sort by score
        sorted_formats = sorted(format_scores.items(), key=lambda x: x[1], reverse=True)
        
        best_format = sorted_formats[0][0]
        best_score = sorted_formats[0][1]
        
        # Get alternatives (formats within 20 points)
        alternatives = [
            fmt for fmt, score in sorted_formats[1:]
            if score >= best_score - 20
        ][:2]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            best_format,
            self.formats[best_format],
            topic_lower,
            best_score
        )
        
        # Calculate confidence
        confidence = min(95, max(50, best_score))
        
        return FormatRecommendation(
            recommended_format=best_format,
            confidence=round(confidence, 2),
            alternative_formats=alternatives,
            reasoning=reasoning,
            format_details=self.formats[best_format]
        )
    
    def _score_format(
        self,
        format_name: str,
        format_info: dict,
        topic: str,
        niche: str,
        audience: str,
        desired_length: int,
        capacity: str
    ) -> float:
        """Score a format for the given parameters."""
        score = 50.0  # Base score
        
        # Topic match
        best_for = format_info["best_for"]
        topic_matches = sum(1 for bf in best_for if bf in topic)
        score += topic_matches * 15
        
        # Length compatibility
        if desired_length > 0:
            min_len, max_len = format_info["length_range"]
            if min_len <= desired_length <= max_len:
                score += 20
            elif abs(desired_length - min_len) < 100 or abs(desired_length - max_len) < 100:
                score += 10
        
        # Audience match
        audience_keywords = {
            "engaged learners": ["learn", "understand", "deep", "detailed"],
            "general": ["intro", "overview", "basics"],
            "buyers": ["review", "best", "compare", "buy"],
            "visual learners": ["see", "visual", "show", "demonstrate"]
        }
        
        target_audience = format_info["audience"]
        if target_audience in audience_keywords:
            keywords = audience_keywords[target_audience]
            if any(kw in topic for kw in keywords):
                score += 15
        
        # Production capacity adjustment
        complexity = format_info["complexity"]
        if capacity == "low" and complexity == "high":
            score -= 20
        elif capacity == "high" and complexity == "high":
            score += 10
        
        return min(100, max(0, score))
    
    def _generate_reasoning(
        self,
        format_name: str,
        format_info: dict,
        topic: str,
        score: float
    ) -> List[str]:
        """Generate reasoning for format recommendation."""
        reasons = []
        
        # Topic alignment
        best_for = format_info["best_for"]
        matches = [bf for bf in best_for if bf in topic]
        if matches:
            reasons.append(f"Excellent fit for {matches[0]} content")
        
        # Length appropriateness
        min_len, max_len = format_info["length_range"]
        reasons.append(f"Ideal length: {min_len//60}-{max_len//60} minutes")
        
        # Complexity note
        complexity = format_info["complexity"]
        reasons.append(f"{complexity.capitalize()} complexity level")
        
        # Research requirement
        research = format_info["research_required"]
        reasons.append(f"Requires {research} research")
        
        # Audience fit
        reasons.append(f"Best for {format_info['audience']}")
        
        return reasons
    
    def get_all_formats(self) -> List[str]:
        """Get list of all available formats."""
        return list(self.formats.keys())
    
    def get_format_details(self, format_name: str) -> Optional[dict]:
        """Get detailed information about a format."""
        return self.formats.get(format_name.lower())
