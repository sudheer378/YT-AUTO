"""RPM Estimation Engine for YouTube content."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class RPMEstimate:
    """RPM estimation result."""
    
    estimated_rpm: float  # USD per 1000 views
    rpm_score: float  # 0-100
    niche_multiplier: float
    country_multiplier: float
    audience_multiplier: float
    seasonality_factor: float
    factors: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.75


class RPMEstimator:
    """Estimates Revenue Per Mille (RPM) for YouTube content."""
    
    # Base RPM by niche (USD)
    NICHE_BASE_RPM = {
        "finance": 15.0,
        "business": 12.0,
        "technology": 8.0,
        "ai": 9.0,
        "marketing": 10.0,
        "real_estate": 14.0,
        "legal": 16.0,
        "insurance": 18.0,
        "health": 7.0,
        "fitness": 5.0,
        "education": 4.0,
        "science": 6.0,
        "documentary": 5.0,
        "entertainment": 3.0,
        "gaming": 2.5,
        "vlog": 2.0,
        "comedy": 2.5,
        "music": 2.0,
        "lifestyle": 3.5,
        "travel": 4.0,
        "food": 3.5,
        "general": 3.0,
    }
    
    # Country multipliers
    COUNTRY_MULTIPLIERS = {
        "USA": 1.0,
        "Canada": 0.85,
        "UK": 0.80,
        "Australia": 0.75,
        "Germany": 0.70,
        "France": 0.65,
        "Japan": 0.60,
        "South Korea": 0.55,
        "Brazil": 0.30,
        "Mexico": 0.25,
        "India": 0.20,
    }
    
    # Audience type multipliers
    AUDIENCE_MULTIPLIERS = {
        "business_owners": 1.5,
        "professionals": 1.3,
        "investors": 1.6,
        "students": 0.7,
        "teens": 0.6,
        "kids": 0.4,
        "parents": 1.0,
        "gamers": 0.8,
        "general": 1.0,
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def estimate(
        self,
        niche: str,
        sub_niche: str = "",
        country: str = "USA",
        audience_type: str = "general",
        video_length_seconds: int = 600,
        is_seasonal: bool = False
    ) -> RPMEstimate:
        """
        Estimate RPM based on multiple factors.
        
        Args:
            niche: Content niche
            sub_niche: Specific sub-niche
            country: Target country
            audience_type: Primary audience type
            video_length_seconds: Video length
            is_seasonal: Whether content is seasonal
            
        Returns:
            RPMEstimate with detailed breakdown
        """
        logger.info(f"Estimating RPM for {niche} in {country}")
        
        # Get base RPM for niche
        niche_lower = niche.lower()
        base_rpm = self.NICHE_BASE_RPM.get(niche_lower, self.NICHE_BASE_RPM["general"])
        
        # Apply sub-niche adjustment
        niche_multiplier = self._calculate_niche_multiplier(niche, sub_niche)
        
        # Country multiplier
        country_multiplier = self.COUNTRY_MULTIPLIERS.get(country, 0.5)
        
        # Audience multiplier
        audience_multiplier = self.AUDIENCE_MULTIPLIERS.get(audience_type, 1.0)
        
        # Video length factor (longer videos can have more mid-roll ads)
        length_factor = 1.0
        if video_length_seconds > 480:  # Over 8 minutes
            length_factor = 1.3
        elif video_length_seconds > 300:  # Over 5 minutes
            length_factor = 1.1
        
        # Seasonality factor
        seasonality_factor = 1.2 if is_seasonal else 1.0
        
        # Calculate final RPM
        estimated_rpm = (
            base_rpm *
            niche_multiplier *
            country_multiplier *
            audience_multiplier *
            length_factor *
            seasonality_factor
        )
        
        # Clamp to realistic range
        estimated_rpm = max(0.50, min(50.0, estimated_rpm))
        
        # Calculate RPM score (0-100)
        rpm_score = min(100, (estimated_rpm / 20.0) * 100)
        
        # Compile factors
        factors = {
            "base_rpm": base_rpm,
            "niche_multiplier": niche_multiplier,
            "country_multiplier": country_multiplier,
            "audience_multiplier": audience_multiplier,
            "length_factor": length_factor,
            "seasonality_factor": seasonality_factor,
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            niche, country, audience_type, estimated_rpm
        )
        
        return RPMEstimate(
            estimated_rpm=round(estimated_rpm, 2),
            rpm_score=round(rpm_score, 2),
            niche_multiplier=round(niche_multiplier, 2),
            country_multiplier=round(country_multiplier, 2),
            audience_multiplier=round(audience_multiplier, 2),
            seasonality_factor=round(seasonality_factor, 2),
            factors=factors,
            recommendations=recommendations,
            confidence=0.75
        )
    
    def _calculate_niche_multiplier(self, niche: str, sub_niche: str) -> float:
        """Calculate niche-specific multiplier."""
        multiplier = 1.0
        
        niche_lower = niche.lower()
        sub_niche_lower = sub_niche.lower() if sub_niche else ""
        
        # High-value sub-niches
        high_value_subniches = [
            "investing", "trading", "crypto", "stocks",
            "saas", "startup", "entrepreneurship",
            "machine learning", "artificial intelligence",
            "digital marketing", "seo",
            "personal finance", "wealth building"
        ]
        
        if any(sn in sub_niche_lower for sn in high_value_subniches):
            multiplier = 1.3
        
        # Premium niches get boost
        if niche_lower in ["finance", "business", "legal", "insurance"]:
            multiplier = max(multiplier, 1.2)
        
        return multiplier
    
    def _generate_recommendations(
        self,
        niche: str,
        country: str,
        audience_type: str,
        estimated_rpm: float
    ) -> List[str]:
        """Generate recommendations to improve RPM."""
        recommendations = []
        
        # Country-based recommendations
        if country not in ["USA", "Canada", "UK", "Australia"]:
            recommendations.append(
                f"Consider creating content targeting USA/UK audiences for higher RPM "
                f"(current: {country})"
            )
        
        # Niche-based recommendations
        niche_lower = niche.lower()
        if niche_lower in ["gaming", "entertainment", "comedy", "music"]:
            recommendations.append(
                "Consider adding educational or business angles to increase RPM potential"
            )
        
        # Audience-based recommendations
        if audience_type in ["kids", "teens", "students"]:
            recommendations.append(
                "Content for professionals/business owners typically has 2-3x higher RPM"
            )
        
        # Length recommendation
        if estimated_rpm < 5.0:
            recommendations.append(
                "Create videos over 8 minutes to enable mid-roll ad placements"
            )
        
        # General optimization
        if estimated_rpm < 3.0:
            recommendations.append(
                "Focus on high-value niches: finance, business, technology, or education"
            )
        
        return recommendations[:5]
    
    def compare_niches(self, niches: List[str], country: str = "USA") -> Dict[str, float]:
        """Compare RPM potential across multiple niches."""
        comparison = {}
        for niche in niches:
            estimate = self.estimate(niche=niche, country=country)
            comparison[niche] = estimate.estimated_rpm
        return comparison
    
    def get_top_niches(self, country: str = "USA", limit: int = 10) -> List[tuple]:
        """Get top RPM niches for a country."""
        results = []
        for niche in self.NICHE_BASE_RPM.keys():
            estimate = self.estimate(niche=niche, country=country)
            results.append((niche, estimate.estimated_rpm))
        
        # Sort by RPM descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
