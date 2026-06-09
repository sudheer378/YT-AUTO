"""Advertiser Score for content monetization safety."""

from dataclasses import dataclass, field
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdvertiserScoreResult:
    """Advertiser friendliness score."""
    
    score: float  # 0-100
    rating: str  # "Green", "Yellow", "Red"
    brand_safe: bool
    factors: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class AdvertiserScorer:
    """Scores content for advertiser friendliness."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Sensitive topics that reduce advertiser appeal
        self.sensitive_topics = [
            "violence", "war", "conflict", "weapons",
            "drugs", "alcohol", "smoking",
            "adult", "sexual", "nsfw",
            "controversial", "political", "conspiracy",
            "tragedy", "disaster", "death",
            "gambling", "casino", "betting",
            "get rich quick", "pyramid", "scam"
        ]
        
        # Positive advertiser-friendly topics
        self.positive_topics = [
            "education", "tutorial", "how to", "guide",
            "review", "comparison", "best",
            "technology", "science", "innovation",
            "business", "entrepreneurship", "career",
            "health", "fitness", "wellness",
            "travel", "food", "lifestyle"
        ]
    
    def score(
        self,
        title: str,
        description: str = "",
        script: str = "",
        niche: str = "general"
    ) -> AdvertiserScoreResult:
        """
        Calculate advertiser friendliness score.
        
        Args:
            title: Video title
            description: Video description
            script: Video script
            niche: Content niche
            
        Returns:
            AdvertiserScoreResult with detailed breakdown
        """
        logger.info(f"Calculating advertiser score for: {title[:50]}...")
        
        # Combine text for analysis
        full_text = f"{title} {description} {script}".lower()
        
        # Analyze factors
        sensitive_score = self._analyze_sensitive_content(full_text)
        positive_score = self._analyze_positive_content(full_text)
        niche_score = self._get_niche_advertiser_score(niche)
        language_score = self._analyze_language(full_text)
        
        # Calculate final score
        final_score = (
            sensitive_score * 0.4 +
            positive_score * 0.3 +
            niche_score * 0.2 +
            language_score * 0.1
        )
        
        # Clamp to 0-100
        final_score = max(0, min(100, final_score))
        
        # Determine rating
        if final_score >= 75:
            rating = "Green"
            brand_safe = True
        elif final_score >= 50:
            rating = "Yellow"
            brand_safe = True
        else:
            rating = "Red"
            brand_safe = False
        
        # Compile factors
        factors = {
            "sensitive_content": sensitive_score,
            "positive_content": positive_score,
            "niche_appeal": niche_score,
            "language_appropriateness": language_score,
        }
        
        # Generate warnings and recommendations
        warnings = self._generate_warnings(full_text, sensitive_score)
        recommendations = self._generate_recommendations(
            full_text, final_score, warnings
        )
        
        return AdvertiserScoreResult(
            score=round(final_score, 2),
            rating=rating,
            brand_safe=brand_safe,
            factors=factors,
            warnings=warnings,
            recommendations=recommendations
        )
    
    def _analyze_sensitive_content(self, text: str) -> float:
        """Analyze presence of sensitive content (higher is better)."""
        sensitive_count = sum(1 for topic in self.sensitive_topics if topic in text)
        
        # More sensitive topics = lower score
        if sensitive_count == 0:
            return 100
        elif sensitive_count <= 2:
            return 80
        elif sensitive_count <= 4:
            return 60
        elif sensitive_count <= 6:
            return 40
        else:
            return 20
    
    def _analyze_positive_content(self, text: str) -> float:
        """Analyze presence of advertiser-friendly content."""
        positive_count = sum(1 for topic in self.positive_topics if topic in text)
        
        if positive_count >= 5:
            return 100
        elif positive_count >= 3:
            return 85
        elif positive_count >= 1:
            return 70
        else:
            return 50
    
    def _get_niche_advertiser_score(self, niche: str) -> float:
        """Get base advertiser score for niche."""
        niche_scores = {
            "technology": 85,
            "ai": 85,
            "education": 90,
            "science": 88,
            "business": 82,
            "finance": 75,
            "health": 70,
            "fitness": 75,
            "travel": 80,
            "food": 85,
            "lifestyle": 75,
            "entertainment": 65,
            "gaming": 60,
            "comedy": 55,
            "vlog": 60,
            "music": 65,
            "general": 70,
        }
        
        return niche_scores.get(niche.lower(), 70)
    
    def _analyze_language(self, text: str) -> float:
        """Analyze language appropriateness."""
        # Check for profanity indicators
        profanity_indicators = [
            "damn", "hell", "crap", "pissed",
            "stupid", "idiot", "dumb"
        ]
        
        profanity_count = sum(1 for word in profanity_indicators if word in text)
        
        if profanity_count == 0:
            return 100
        elif profanity_count <= 2:
            return 80
        elif profanity_count <= 5:
            return 60
        else:
            return 40
    
    def _generate_warnings(self, text: str, sensitive_score: float) -> List[str]:
        """Generate warnings about potential issues."""
        warnings = []
        
        if sensitive_score < 60:
            detected = [topic for topic in self.sensitive_topics if topic in text]
            if detected:
                warnings.append(
                    f"Sensitive topics detected: {', '.join(detected[:3])}"
                )
        
        # Check for excessive negativity
        negative_words = ["terrible", "awful", "horrible", "worst", "hate"]
        negative_count = sum(1 for word in negative_words if word in text)
        if negative_count >= 3:
            warnings.append("High concentration of negative language detected")
        
        # Check for controversial claims
        controversial_phrases = ["they don't want you to know", "secret truth", "exposed"]
        if any(phrase in text for phrase in controversial_phrases):
            warnings.append("Controversial claims may limit monetization")
        
        return warnings
    
    def _generate_recommendations(
        self,
        text: str,
        score: float,
        warnings: List[str]
    ) -> List[str]:
        """Generate recommendations to improve advertiser appeal."""
        recommendations = []
        
        if score < 75:
            recommendations.append(
                "Reduce references to sensitive topics to improve advertiser appeal"
            )
        
        if not any(topic in text for topic in self.positive_topics):
            recommendations.append(
                "Add educational or informative elements to increase brand safety"
            )
        
        if len(warnings) > 0:
            recommendations.append(
                "Review flagged content and consider softer language alternatives"
            )
        
        if score < 60:
            recommendations.append(
                "Consider creating a separate series for more controversial topics"
            )
        
        return recommendations[:4]
    
    def is_monetizable(self, score: float) -> bool:
        """Determine if content is likely to be fully monetized."""
        return score >= 50
    
    def get_demonetization_risk(self, score: float) -> str:
        """Get demonetization risk level."""
        if score >= 75:
            return "Low"
        elif score >= 50:
            return "Medium"
        else:
            return "High"
