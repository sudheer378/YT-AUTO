"""Niche Profitability Analyzer for long-term revenue potential."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class NicheProfitabilityReport:
    """Niche profitability analysis report."""
    
    niche: str
    profitability_score: float  # 0-100
    revenue_potential: str  # "Very High", "High", "Medium", "Low"
    competition_level: str  # "Low", "Medium", "High", "Saturated"
    growth_trajectory: str  # "Growing", "Stable", "Declining"
    monetization_methods: List[str] = field(default_factory=list)
    estimated_monthly_revenue: Tuple[float, float] = field(default=(0, 0))
    barriers_to_entry: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)


class NicheProfitabilityAnalyzer:
    """Analyzes long-term profitability of YouTube niches."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Niche profitability data
        self.niche_data = {
            "finance": {
                "base_score": 92,
                "competition": "High",
                "growth": "Stable",
                "revenue_tier": "Very High",
                "monetization": [
                    "AdSense", "Affiliate Marketing", "Sponsorships",
                    "Digital Products", "Consulting", "Courses"
                ],
                "barriers": ["Expertise required", "Regulatory compliance", "Trust building"],
                "avg_cpm": 15.0,
            },
            "business": {
                "base_score": 88,
                "competition": "High",
                "growth": "Growing",
                "revenue_tier": "Very High",
                "monetization": [
                    "AdSense", "Sponsorships", "Affiliate Marketing",
                    "B2B Services", "Courses", "Coaching"
                ],
                "barriers": ["Business experience", "Network required"],
                "avg_cpm": 12.0,
            },
            "technology": {
                "base_score": 82,
                "competition": "High",
                "growth": "Growing",
                "revenue_tier": "High",
                "monetization": [
                    "AdSense", "Sponsorships", "Affiliate Marketing",
                    "Product Reviews", "Tech Consulting"
                ],
                "barriers": ["Technical knowledge", "Equipment costs"],
                "avg_cpm": 8.0,
            },
            "ai": {
                "base_score": 85,
                "competition": "Medium",
                "growth": "Rapidly Growing",
                "revenue_tier": "High",
                "monetization": [
                    "AdSense", "Sponsorships", "Affiliate Marketing",
                    "AI Tools", "Courses", "Consulting"
                ],
                "barriers": ["Rapid learning curve", "Technical understanding"],
                "avg_cpm": 9.0,
            },
            "health": {
                "base_score": 75,
                "competition": "High",
                "growth": "Stable",
                "revenue_tier": "High",
                "monetization": [
                    "AdSense", "Sponsorships", "Affiliate Marketing",
                    "Fitness Programs", "Supplements"
                ],
                "barriers": ["Credentials may be required", "Medical disclaimers"],
                "avg_cpm": 7.0,
            },
            "education": {
                "base_score": 78,
                "competition": "Medium",
                "growth": "Growing",
                "revenue_tier": "Medium",
                "monetization": [
                    "AdSense", "Sponsorships", "Online Courses",
                    "Tutoring", "Educational Materials"
                ],
                "barriers": ["Subject expertise", "Teaching ability"],
                "avg_cpm": 4.0,
            },
            "entertainment": {
                "base_score": 55,
                "competition": "Saturated",
                "growth": "Stable",
                "revenue_tier": "Medium",
                "monetization": [
                    "AdSense", "Sponsorships", "Merchandise",
                    "Fan Funding", "Brand Deals"
                ],
                "barriers": ["High competition", "Personality-driven"],
                "avg_cpm": 3.0,
            },
            "gaming": {
                "base_score": 52,
                "competition": "Saturated",
                "growth": "Stable",
                "revenue_tier": "Medium",
                "monetization": [
                    "AdSense", "Sponsorships", "Donations",
                    "Merchandise", "Game Affiliate"
                ],
                "barriers": ["Gaming equipment", "High competition", "Consistency required"],
                "avg_cpm": 2.5,
            },
            "lifestyle": {
                "base_score": 65,
                "competition": "High",
                "growth": "Stable",
                "revenue_tier": "Medium",
                "monetization": [
                    "AdSense", "Sponsorships", "Affiliate Marketing",
                    "Brand Partnerships", "Products"
                ],
                "barriers": ["Aesthetic requirements", "Lifestyle investment"],
                "avg_cpm": 3.5,
            },
            "general": {
                "base_score": 60,
                "competition": "Medium",
                "growth": "Stable",
                "revenue_tier": "Medium",
                "monetization": [
                    "AdSense", "Sponsorships", "Affiliate Marketing"
                ],
                "barriers": ["Finding unique angle"],
                "avg_cpm": 3.0,
            },
        }
    
    def analyze(
        self,
        niche: str,
        sub_niche: str = "",
        current_subscribers: int = 0,
        upload_frequency: int = 4
    ) -> NicheProfitabilityReport:
        """
        Analyze niche profitability.
        
        Args:
            niche: Target niche
            sub_niche: Specific sub-niche
            current_subscribers: Current subscriber count
            upload_frequency: Videos per month
            
        Returns:
            NicheProfitabilityReport with comprehensive analysis
        """
        logger.info(f"Analyzing profitability for niche: {niche}")
        
        niche_lower = niche.lower()
        data = self.niche_data.get(niche_lower, self.niche_data["general"])
        
        # Calculate profitability score
        base_score = data["base_score"]
        
        # Adjust for sub-niche
        if sub_niche:
            base_score = self._adjust_for_sub_niche(base_score, sub_niche)
        
        # Adjust for competition
        competition_adjustment = self._get_competition_adjustment(data["competition"])
        
        # Adjust for growth trajectory
        growth_adjustment = self._get_growth_adjustment(data["growth"])
        
        # Final score
        profitability_score = base_score * competition_adjustment * growth_adjustment
        profitability_score = max(0, min(100, profitability_score))
        
        # Revenue potential
        revenue_potential = data["revenue_tier"]
        
        # Estimated monthly revenue range
        estimated_revenue = self._estimate_revenue(
            data["avg_cpm"],
            upload_frequency,
            current_subscribers
        )
        
        # Risk factors
        risk_factors = self._identify_risks(niche_lower, data)
        
        # Recommendations
        recommendations = self._generate_recommendations(
            niche_lower, profitability_score, data
        )
        
        return NicheProfitabilityReport(
            niche=niche,
            profitability_score=round(profitability_score, 2),
            revenue_potential=revenue_potential,
            competition_level=data["competition"],
            growth_trajectory=data["growth"],
            monetization_methods=data["monetization"],
            estimated_monthly_revenue=estimated_revenue,
            barriers_to_entry=data["barriers"],
            recommendations=recommendations,
            risk_factors=risk_factors
        )
    
    def _adjust_for_sub_niche(self, base_score: float, sub_niche: str) -> float:
        """Adjust score based on sub-niche specificity."""
        premium_subniches = [
            "investing", "trading", "crypto", "stocks",
            "saas", "startup", "machine learning",
            "artificial intelligence", "b2b"
        ]
        
        sub_niche_lower = sub_niche.lower()
        
        if any(sn in sub_niche_lower for sn in premium_subniches):
            return min(100, base_score + 5)
        
        return base_score
    
    def _get_competition_adjustment(self, competition: str) -> float:
        """Get adjustment factor for competition level."""
        adjustments = {
            "Low": 1.1,
            "Medium": 1.0,
            "High": 0.95,
            "Saturated": 0.9,
        }
        return adjustments.get(competition, 1.0)
    
    def _get_growth_adjustment(self, growth: str) -> float:
        """Get adjustment factor for growth trajectory."""
        adjustments = {
            "Rapidly Growing": 1.15,
            "Growing": 1.05,
            "Stable": 1.0,
            "Declining": 0.85,
        }
        return adjustments.get(growth, 1.0)
    
    def _estimate_revenue(
        self,
        avg_cpm: float,
        upload_frequency: int,
        subscribers: int
    ) -> Tuple[float, float]:
        """Estimate monthly revenue range."""
        # Base views estimate (varies widely, so we give a range)
        if subscribers == 0:
            min_views = 1000 * upload_frequency
            max_views = 10000 * upload_frequency
        else:
            min_views = subscribers * 0.3 * upload_frequency
            max_views = subscribers * 1.5 * upload_frequency
        
        # Calculate revenue (CPM / 1000 * views)
        min_revenue = (avg_cpm / 1000) * min_views
        max_revenue = (avg_cpm / 1000) * max_views
        
        return (round(min_revenue, 2), round(max_revenue, 2))
    
    def _identify_risks(self, niche: str, data: dict) -> List[str]:
        """Identify potential risks for the niche."""
        risks = []
        
        if data["competition"] == "Saturated":
            risks.append("High competition makes discovery difficult")
        
        if data["growth"] == "Declining":
            risks.append("Niche may be losing audience interest")
        
        if niche in ["finance", "health"]:
            risks.append("Regulatory and compliance considerations")
        
        if niche in ["entertainment", "gaming"]:
            risks.append("Revenue heavily dependent on personality/brand")
        
        return risks
    
    def _generate_recommendations(
        self,
        niche: str,
        score: float,
        data: dict
    ) -> List[str]:
        """Generate strategic recommendations."""
        recommendations = []
        
        if score >= 80:
            recommendations.append(
                f"Excellent niche choice ({score}/100). Focus on consistent quality content."
            )
        elif score >= 65:
            recommendations.append(
                f"Good niche potential ({score}/100). Differentiate through unique perspective."
            )
        else:
            recommendations.append(
                f"Consider specializing in a sub-niche to improve profitability."
            )
        
        # Monetization recommendations
        if len(data["monetization"]) > 3:
            recommendations.append(
                f"Diversify revenue streams: leverage {len(data['monetization'])} monetization methods available"
            )
        
        # Competition-based advice
        if data["competition"] in ["High", "Saturated"]:
            recommendations.append(
                "Focus on underserved sub-topics within this niche"
            )
        
        return recommendations[:5]
    
    def compare_niches(self, niches: List[str]) -> List[NicheProfitabilityReport]:
        """Compare multiple niches side by side."""
        reports = []
        for niche in niches:
            report = self.analyze(niche)
            reports.append(report)
        
        # Sort by profitability score
        reports.sort(key=lambda r: r.profitability_score, reverse=True)
        
        return reports
    
    def get_top_niches(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Get top niches by profitability score."""
        results = []
        for niche, data in self.niche_data.items():
            results.append((niche, data["base_score"]))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
