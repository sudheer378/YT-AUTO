"""RPM Scoring for monetization analysis."""

from dataclasses import dataclass, field
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class RPMScore:
    """RPM scoring result."""
    
    score: float  # 0-100
    estimated_rpm: float
    tier: str  # "Premium", "High", "Medium", "Low"
    factors: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class RPMScorer:
    """Scores content for RPM potential."""
    
    # RPM tiers
    PREMIUM_RPM = 15.0
    HIGH_RPM = 8.0
    MEDIUM_RPM = 4.0
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def score(
        self,
        niche: str,
        sub_niche: str = "",
        country: str = "USA",
        audience_type: str = "general",
        topic: str = ""
    ) -> RPMScore:
        """
        Calculate RPM score for content.
        
        Args:
            niche: Content niche
            sub_niche: Specific sub-niche
            country: Target country
            audience_type: Primary audience type
            topic: Specific topic
            
        Returns:
            RPMScore with detailed breakdown
        """
        logger.info(f"Calculating RPM score for {niche} in {country}")
        
        # Base score from niche
        base_score = self._get_niche_base_score(niche)
        
        # Adjustments
        country_factor = self._get_country_factor(country)
        audience_factor = self._get_audience_factor(audience_type)
        sub_niche_factor = self._get_sub_niche_factor(sub_niche)
        topic_factor = self._get_topic_factor(topic, niche)
        
        # Calculate final score
        final_score = (
            base_score *
            country_factor *
            audience_factor *
            sub_niche_factor *
            topic_factor
        )
        
        # Clamp to 0-100
        final_score = max(0, min(100, final_score))
        
        # Estimate RPM
        estimated_rpm = (final_score / 100) * 20.0  # Scale to $0-20
        
        # Determine tier
        if estimated_rpm >= self.PREMIUM_RPM:
            tier = "Premium"
        elif estimated_rpm >= self.HIGH_RPM:
            tier = "High"
        elif estimated_rpm >= self.MEDIUM_RPM:
            tier = "Medium"
        else:
            tier = "Low"
        
        # Compile factors
        factors = {
            "base_score": base_score,
            "country_factor": country_factor,
            "audience_factor": audience_factor,
            "sub_niche_factor": sub_niche_factor,
            "topic_factor": topic_factor,
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            niche, country, audience_type, estimated_rpm
        )
        
        return RPMScore(
            score=round(final_score, 2),
            estimated_rpm=round(estimated_rpm, 2),
            tier=tier,
            factors=factors,
            recommendations=recommendations
        )
    
    def _get_niche_base_score(self, niche: str) -> float:
        """Get base score for niche."""
        niche_scores = {
            "finance": 90,
            "business": 85,
            "legal": 88,
            "insurance": 92,
            "real_estate": 87,
            "technology": 75,
            "ai": 78,
            "marketing": 80,
            "health": 65,
            "education": 60,
            "science": 62,
            "fitness": 55,
            "lifestyle": 50,
            "travel": 52,
            "food": 48,
            "entertainment": 40,
            "gaming": 38,
            "comedy": 35,
            "music": 32,
            "vlog": 30,
            "general": 50,
        }
        
        return niche_scores.get(niche.lower(), 50)
    
    def _get_country_factor(self, country: str) -> float:
        """Get country multiplier factor."""
        country_factors = {
            "USA": 1.0,
            "Canada": 0.9,
            "UK": 0.85,
            "Australia": 0.8,
            "Germany": 0.75,
            "France": 0.7,
            "Japan": 0.65,
            "South Korea": 0.6,
            "Brazil": 0.4,
            "Mexico": 0.35,
            "India": 0.3,
        }
        
        return country_factors.get(country, 0.5)
    
    def _get_audience_factor(self, audience_type: str) -> float:
        """Get audience type factor."""
        audience_factors = {
            "business_owners": 1.4,
            "investors": 1.5,
            "professionals": 1.2,
            "parents": 1.0,
            "general": 1.0,
            "gamers": 0.85,
            "students": 0.75,
            "teens": 0.7,
            "kids": 0.5,
        }
        
        return audience_factors.get(audience_type, 1.0)
    
    def _get_sub_niche_factor(self, sub_niche: str) -> float:
        """Get sub-niche adjustment factor."""
        if not sub_niche:
            return 1.0
        
        sub_niche_lower = sub_niche.lower()
        
        premium_subniches = [
            "investing", "trading", "crypto", "stocks",
            "saas", "startup", "entrepreneurship",
            "machine learning", "artificial intelligence",
            "digital marketing", "seo",
            "personal finance", "wealth building",
            "b2b", "enterprise"
        ]
        
        if any(sn in sub_niche_lower for sn in premium_subniches):
            return 1.2
        
        return 1.0
    
    def _get_topic_factor(self, topic: str, niche: str) -> float:
        """Get topic-specific factor."""
        if not topic:
            return 1.0
        
        topic_lower = topic.lower()
        
        # High-value topic indicators
        high_value_keywords = [
            "make money", "invest", "business", "profit",
            "software", "tool", "platform", "service",
            "review", "comparison", "best", "top",
            "tutorial", "course", "training"
        ]
        
        keyword_count = sum(1 for kw in high_value_keywords if kw in topic_lower)
        
        if keyword_count >= 3:
            return 1.15
        elif keyword_count >= 1:
            return 1.05
        
        return 1.0
    
    def _generate_recommendations(
        self,
        niche: str,
        country: str,
        audience_type: str,
        estimated_rpm: float
    ) -> List[str]:
        """Generate RPM improvement recommendations."""
        recommendations = []
        
        if estimated_rpm < 5.0:
            recommendations.append(
                "Consider targeting higher-value niches like finance, business, or technology"
            )
        
        if country not in ["USA", "Canada", "UK", "Australia"]:
            recommendations.append(
                f"Content targeting Tier 1 countries (USA, UK, Canada, Australia) "
                f"typically earns 2-3x more"
            )
        
        if audience_type in ["kids", "teens", "students"]:
            recommendations.append(
                "Business and professional audiences generate higher ad revenue"
            )
        
        if estimated_rpm < 8.0:
            recommendations.append(
                "Add product reviews, comparisons, or tutorials to increase advertiser interest"
            )
        
        return recommendations[:4]
