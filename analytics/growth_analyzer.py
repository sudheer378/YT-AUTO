"""Growth Analysis Engine for YouTube channels."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class GrowthForecast:
    """Growth forecast result."""
    
    current_subscribers: int
    projected_30_days: int
    projected_90_days: int
    projected_180_days: int
    growth_rate_monthly: float  # Percentage
    consistency_score: float  # 0-100
    niche_saturation_score: float  # 0-100 (lower is better)
    view_potential: int
    factors: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.70


@dataclass
class MilestoneProjection:
    """Channel milestone projection."""
    
    milestone: int
    estimated_date: str
    days_until: int
    confidence: float


class GrowthAnalyzer:
    """Analyzes and projects channel growth potential."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Growth rate benchmarks by niche
        self.niche_growth_benchmarks = {
            "technology": 0.15,
            "ai": 0.20,
            "finance": 0.12,
            "business": 0.14,
            "education": 0.18,
            "entertainment": 0.25,
            "gaming": 0.22,
            "lifestyle": 0.16,
            "health": 0.13,
            "fitness": 0.17,
            "general": 0.10,
        }
    
    def forecast(
        self,
        current_subscribers: int,
        current_views_monthly: int,
        niche: str,
        upload_frequency: int,  # Videos per month
        avg_video_length: int = 600,  # seconds
        ctr_estimate: float = 5.0,
        retention_estimate: float = 50.0,
        consistency_score: float = 50.0
    ) -> GrowthForecast:
        """
        Forecast channel growth over multiple timeframes.
        
        Args:
            current_subscribers: Current subscriber count
            current_views_monthly: Current monthly views
            niche: Channel niche
            upload_frequency: Videos per month
            avg_video_length: Average video length in seconds
            ctr_estimate: Estimated CTR percentage
            retention_estimate: Estimated retention percentage
            consistency_score: Upload consistency score (0-100)
            
        Returns:
            GrowthForecast with projections
        """
        logger.info(f"Forecasting growth for {current_subscribers} subs in {niche}")
        
        # Get base growth rate for niche
        base_growth_rate = self.niche_growth_benchmarks.get(
            niche.lower(), 
            self.niche_growth_benchmarks["general"]
        )
        
        # Adjust for upload frequency
        frequency_factor = min(2.0, upload_frequency / 4.0)  # 4 videos/month is baseline
        
        # Adjust for CTR
        ctr_factor = ctr_estimate / 5.0  # 5% is baseline
        
        # Adjust for retention
        retention_factor = retention_estimate / 50.0  # 50% is baseline
        
        # Consistency factor
        consistency_factor = consistency_score / 50.0
        
        # Calculate effective growth rate
        effective_growth_rate = (
            base_growth_rate *
            frequency_factor *
            ctr_factor *
            retention_factor *
            consistency_factor
        )
        
        # Clamp growth rate
        effective_growth_rate = max(0.02, min(0.50, effective_growth_rate))
        
        # Project growth
        projected_30 = self._project_growth(
            current_subscribers, effective_growth_rate, 1
        )
        projected_90 = self._project_growth(
            current_subscribers, effective_growth_rate, 3
        )
        projected_180 = self._project_growth(
            current_subscribers, effective_growth_rate, 6
        )
        
        # Calculate view potential
        view_potential = self._estimate_view_potential(
            projected_90, niche, upload_frequency
        )
        
        # Calculate niche saturation
        niche_saturation = self._calculate_niche_saturation(niche)
        
        # Compile factors
        factors = {
            "base_growth_rate": base_growth_rate,
            "frequency_factor": frequency_factor,
            "ctr_factor": ctr_factor,
            "retention_factor": retention_factor,
            "consistency_factor": consistency_factor,
            "effective_growth_rate": effective_growth_rate,
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            niche, upload_frequency, ctr_estimate, retention_estimate, consistency_score
        )
        
        return GrowthForecast(
            current_subscribers=current_subscribers,
            projected_30_days=projected_30,
            projected_90_days=projected_90,
            projected_180_days=projected_180,
            growth_rate_monthly=round(effective_growth_rate * 100, 2),
            consistency_score=round(consistency_score, 2),
            niche_saturation_score=round(niche_saturation, 2),
            view_potential=view_potential,
            factors=factors,
            recommendations=recommendations,
            confidence=0.70
        )
    
    def _project_growth(
        self, 
        current: int, 
        monthly_rate: float, 
        months: int
    ) -> int:
        """Project subscriber growth over time."""
        projected = current
        for _ in range(months):
            projected = int(projected * (1 + monthly_rate))
        return projected
    
    def _estimate_view_potential(
        self,
        projected_subs: int,
        niche: str,
        upload_frequency: int
    ) -> int:
        """Estimate potential monthly views based on subscribers."""
        # Average views per subscriber varies by niche
        vps_by_niche = {
            "technology": 0.8,
            "ai": 1.0,
            "finance": 0.6,
            "business": 0.7,
            "education": 1.2,
            "entertainment": 1.5,
            "gaming": 2.0,
            "lifestyle": 1.0,
            "health": 0.8,
            "fitness": 0.9,
            "general": 0.7,
        }
        
        vps = vps_by_niche.get(niche.lower(), 0.7)
        
        # Base views from subscribers
        base_views = projected_subs * vps
        
        # Additional views from non-subscribers (typically 30-50% of total)
        total_views = int(base_views / 0.6)  # Subs represent ~60% of views
        
        # Adjust for upload frequency
        frequency_adjustment = min(2.0, upload_frequency / 4.0)
        
        return int(total_views * frequency_adjustment)
    
    def _calculate_niche_saturation(self, niche: str) -> float:
        """Calculate niche saturation score (0-100, lower is better)."""
        saturation_levels = {
            "gaming": 85,
            "entertainment": 80,
            "vlog": 75,
            "comedy": 70,
            "music": 75,
            "technology": 60,
            "ai": 40,  # Emerging niche
            "finance": 55,
            "business": 50,
            "education": 45,
            "health": 50,
            "fitness": 65,
            "lifestyle": 70,
            "travel": 60,
            "food": 65,
            "general": 50,
        }
        
        return saturation_levels.get(niche.lower(), 50)
    
    def _generate_recommendations(
        self,
        niche: str,
        upload_frequency: int,
        ctr_estimate: float,
        retention_estimate: float,
        consistency_score: float
    ) -> List[str]:
        """Generate growth recommendations."""
        recommendations = []
        
        # Upload frequency
        if upload_frequency < 4:
            recommendations.append(
                "Increase upload frequency to at least 4 videos per month for optimal growth"
            )
        
        # CTR optimization
        if ctr_estimate < 5.0:
            recommendations.append(
                "Focus on improving CTR through better thumbnails and titles (target: 5%+)"
            )
        
        # Retention optimization
        if retention_estimate < 50.0:
            recommendations.append(
                "Improve retention by strengthening hooks and pacing (target: 50%+)"
            )
        
        # Consistency
        if consistency_score < 60.0:
            recommendations.append(
                "Maintain consistent upload schedule to build audience expectations"
            )
        
        # Niche-specific
        niche_lower = niche.lower()
        if niche_lower == "ai":
            recommendations.append(
                "AI niche is growing rapidly - capitalize on trending topics quickly"
            )
        elif niche_lower in ["gaming", "entertainment"]:
            recommendations.append(
                "High saturation niche - focus on unique angles and personality-driven content"
            )
        
        return recommendations[:5]
    
    def project_milestones(
        self,
        current_subscribers: int,
        monthly_growth_rate: float,
        milestones: List[int] = None
    ) -> List[MilestoneProjection]:
        """Project dates for reaching subscriber milestones."""
        if milestones is None:
            milestones = [1000, 10000, 100000, 500000, 1000000]
        
        projections = []
        current_date = datetime.now()
        
        for milestone in milestones:
            if milestone <= current_subscribers:
                continue
            
            # Calculate months needed
            months_needed = 0
            projected = current_subscribers
            while projected < milestone and months_needed < 60:
                projected = int(projected * (1 + monthly_growth_rate))
                months_needed += 1
            
            if months_needed < 60:
                estimated_date = current_date + timedelta(days=months_needed * 30)
                projections.append(MilestoneProjection(
                    milestone=milestone,
                    estimated_date=estimated_date.strftime("%Y-%m-%d"),
                    days_until=months_needed * 30,
                    confidence=max(0.5, 0.9 - (months_needed * 0.01))
                ))
        
        return projections
    
    def compare_strategies(
        self,
        current_subscribers: int,
        niche: str,
        strategies: List[Dict]
    ) -> Dict[str, GrowthForecast]:
        """Compare different growth strategies."""
        results = {}
        
        for strategy in strategies:
            forecast = self.forecast(
                current_subscribers=current_subscribers,
                niche=niche,
                **strategy
            )
            strategy_name = strategy.get("name", "Default")
            results[strategy_name] = forecast
        
        return results
