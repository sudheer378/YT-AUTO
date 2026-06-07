"""Topic Ranker - Ranks and prioritizes topics."""

from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import Opportunity
from .demand_validator import DemandMetrics
from .niche_gap_finder import NicheGap


logger = get_logger(__name__)


@dataclass
class RankedTopic:
    """Represents a ranked topic opportunity."""
    title: str
    description: str
    opportunity_score: float
    trend_score: float
    demand_score: float
    gap_score: float
    feasibility_score: float
    keywords: List[str]
    niche: str
    format_recommendation: str
    estimated_effort: str
    potential_reach: int


class TopicRanker(BaseEngine):
    """Ranks and prioritizes content opportunities."""
    
    def __init__(self):
        super().__init__("topic_ranker")
        self.weights = {
            "trend": 0.25,
            "demand": 0.30,
            "gap": 0.25,
            "feasibility": 0.20,
        }
    
    async def rank(
        self,
        demand_metrics: List[DemandMetrics],
        niche_gaps: List[NicheGap],
        limit: int = 10,
    ) -> List[RankedTopic]:
        """Rank topics based on multiple factors.
        
        Args:
            demand_metrics: List of demand metrics
            niche_gaps: List of niche gaps
            limit: Maximum number of topics to return
            
        Returns:
            List of RankedTopic objects
        """
        try:
            self.logger.info(f"Ranking topics from {len(demand_metrics)} demand metrics and {len(niche_gaps)} gaps")
            
            ranked_topics = []
            
            # Combine demand metrics and niche gaps to generate topics
            for gap in niche_gaps[:limit]:
                # Find matching demand metrics
                matching_demand = [
                    m for m in demand_metrics
                    if gap.sub_niche.lower() in m.keyword.lower()
                ]
                
                if matching_demand:
                    demand = matching_demand[0]
                else:
                    # Create synthetic demand data
                    demand = DemandMetrics(
                        keyword=gap.sub_niche,
                        search_volume=50000,
                        competition_level=gap.competition,
                        engagement_rate=0.5,
                        monetization_potential=0.6,
                        demand_score=gap.demand,
                        confidence=0.7,
                        sources=["synthetic"],
                    )
                
                topic = await self._create_ranked_topic(gap, demand)
                ranked_topics.append(topic)
            
            # Sort by opportunity score descending
            ranked_topics.sort(key=lambda x: x.opportunity_score, reverse=True)
            
            return ranked_topics[:limit]
            
        except Exception as e:
            self.logger.error(f"Error ranking topics: {e}")
            return []
    
    async def _create_ranked_topic(
        self,
        gap: NicheGap,
        demand: DemandMetrics,
    ) -> RankedTopic:
        """Create a ranked topic from gap and demand data.
        
        Args:
            gap: NicheGap object
            demand: DemandMetrics object
            
        Returns:
            RankedTopic object
        """
        # Calculate feasibility (mock)
        feasibility = 0.7 if gap.entry_difficulty == "Low" else 0.5 if gap.entry_difficulty == "Medium" else 0.3
        
        # Calculate overall opportunity score
        opportunity_score = (
            self.weights["trend"] * demand.demand_score +
            self.weights["demand"] * demand.demand_score +
            self.weights["gap"] * gap.gap_score +
            self.weights["feasibility"] * feasibility
        )
        
        # Determine format recommendation
        format_rec = self._recommend_format(gap.sub_niche)
        
        # Estimate potential reach
        potential_reach = int(demand.search_volume * demand.engagement_rate * 10)
        
        return RankedTopic(
            title=f"The Complete Guide to {gap.sub_niche}",
            description=gap.opportunity_description,
            opportunity_score=opportunity_score,
            trend_score=demand.demand_score,
            demand_score=demand.demand_score,
            gap_score=gap.gap_score,
            feasibility_score=feasibility,
            keywords=gap.recommended_topics,
            niche=gap.niche,
            format_recommendation=format_rec,
            estimated_effort=gap.entry_difficulty,
            potential_reach=potential_reach,
        )
    
    def _recommend_format(self, sub_niche: str) -> str:
        """Recommend content format based on sub-niche.
        
        Args:
            sub_niche: Sub-niche name
            
        Returns:
            Recommended format
        """
        tech_keywords = ["AI", "Web3", "IoT", "Cloud", "Cybersecurity"]
        health_keywords = ["Mental Health", "Fitness", "Nutrition", "Sleep"]
        business_keywords = ["Entrepreneurship", "Marketing", "Finance"]
        
        if any(k.lower() in sub_niche.lower() for k in tech_keywords):
            return "explainer"
        elif any(k.lower() in sub_niche.lower() for k in health_keywords):
            return "documentary"
        elif any(k.lower() in sub_niche.lower() for k in business_keywords):
            return "storytelling"
        else:
            return "explainer"
    
    async def rank_opportunities(
        self,
        opportunities: List[Opportunity],
    ) -> List[Opportunity]:
        """Rank existing opportunities.
        
        Args:
            opportunities: List of Opportunity objects
            
        Returns:
            Sorted list of opportunities
        """
        sorted_opps = sorted(
            opportunities,
            key=lambda x: x.opportunity_score,
            reverse=True,
        )
        return sorted_opps
    
    async def process(self, *args, **kwargs) -> List[RankedTopic]:
        """Process topic ranking request."""
        demand_metrics = kwargs.get("demand_metrics", [])
        niche_gaps = kwargs.get("niche_gaps", [])
        limit = kwargs.get("limit", 10)
        return await self.rank(demand_metrics, niche_gaps, limit)
