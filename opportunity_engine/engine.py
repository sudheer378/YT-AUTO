"""Opportunity Engine - Main orchestrator for opportunity discovery."""

from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import Opportunity, ContentFormat
from .trend_scanner import TrendScanner, TrendData
from .demand_validator import DemandValidator
from .niche_gap_finder import NicheGapFinder
from .topic_ranker import TopicRanker, RankedTopic


logger = get_logger(__name__)


@dataclass
class OpportunityResult:
    """Complete opportunity discovery result."""
    ranked_topics: List[RankedTopic]
    trends: List[TrendData]
    total_opportunities: int
    average_score: float
    top_niche: str
    recommendations: List[str]


class OpportunityEngine(BaseEngine):
    """Main engine for discovering content opportunities."""
    
    def __init__(self):
        super().__init__("opportunity_engine")
        self.trend_scanner = TrendScanner()
        self.demand_validator = DemandValidator()
        self.niche_gap_finder = NicheGapFinder()
        self.topic_ranker = TopicRanker()
    
    async def discover(
        self,
        niche: Optional[str] = None,
        limit: int = 10,
        mode: str = "dynamic",
    ) -> OpportunityResult:
        """Discover content opportunities.
        
        Args:
            niche: Optional niche to focus on
            limit: Maximum number of opportunities to return
            mode: Discovery mode ("fixed" or "dynamic")
            
        Returns:
            OpportunityResult object
        """
        try:
            self.logger.info(f"Discovering opportunities for niche: {niche or 'all'}, mode: {mode}")
            
            # Step 1: Scan for trends
            trends = await self.trend_scanner.scan(niche=niche, limit=limit * 2)
            self.logger.info(f"Found {len(trends)} trends")
            
            # Step 2: Validate demand
            demand_metrics = await self.demand_validator.validate(trends)
            self.logger.info(f"Validated {len(demand_metrics)} demand metrics")
            
            # Step 3: Find niche gaps
            niche_gaps = await self.niche_gap_finder.find_gaps(demand_metrics, niche=niche)
            self.logger.info(f"Found {len(niche_gaps)} niche gaps")
            
            # Step 4: Rank topics
            ranked_topics = await self.topic_ranker.rank(demand_metrics, niche_gaps, limit=limit)
            self.logger.info(f"Ranked {len(ranked_topics)} topics")
            
            # Calculate summary statistics
            total_opportunities = len(ranked_topics)
            average_score = sum(t.opportunity_score for t in ranked_topics) / total_opportunities if total_opportunities > 0 else 0
            top_niche = ranked_topics[0].niche if ranked_topics else "Unknown"
            
            # Generate recommendations
            recommendations = self._generate_recommendations(ranked_topics)
            
            return OpportunityResult(
                ranked_topics=ranked_topics,
                trends=trends,
                total_opportunities=total_opportunities,
                average_score=average_score,
                top_niche=top_niche,
                recommendations=recommendations,
            )
            
        except Exception as e:
            self.logger.error(f"Error discovering opportunities: {e}")
            return OpportunityResult(
                ranked_topics=[],
                trends=[],
                total_opportunities=0,
                average_score=0,
                top_niche="Unknown",
                recommendations=["Error during discovery. Please try again."],
            )
    
    def _generate_recommendations(self, topics: List[RankedTopic]) -> List[str]:
        """Generate strategic recommendations based on topics.
        
        Args:
            topics: List of ranked topics
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if not topics:
            return ["No opportunities found. Try adjusting your niche."]
        
        top_topic = topics[0]
        recommendations.append(f"Top opportunity: {top_topic.title} (Score: {top_topic.opportunity_score:.2f})")
        
        # Analyze format distribution
        formats = {}
        for topic in topics:
            fmt = topic.format_recommendation
            formats[fmt] = formats.get(fmt, 0) + 1
        
        if formats:
            top_format = max(formats, key=formats.get)
            recommendations.append(f"Recommended format: {top_format}")
        
        # Difficulty analysis
        easy_topics = [t for t in topics if t.estimated_effort == "Low"]
        if easy_topics:
            recommendations.append(f"{len(easy_topics)} low-effort opportunities available")
        
        return recommendations
    
    async def discover_fixed_niche(
        self,
        niche: str,
        limit: int = 10,
    ) -> OpportunityResult:
        """Discover opportunities in a fixed niche.
        
        Args:
            niche: Niche to focus on
            limit: Maximum opportunities to return
            
        Returns:
            OpportunityResult object
        """
        return await self.discover(niche=niche, limit=limit, mode="fixed")
    
    async def discover_dynamic(self, limit: int = 10) -> OpportunityResult:
        """Discover opportunities across all niches dynamically.
        
        Args:
            limit: Maximum opportunities to return
            
        Returns:
            OpportunityResult object
        """
        return await self.discover(niche=None, limit=limit, mode="dynamic")
    
    async def process(self, *args, **kwargs) -> OpportunityResult:
        """Process opportunity discovery request."""
        niche = kwargs.get("niche")
        limit = kwargs.get("limit", 10)
        mode = kwargs.get("mode", "dynamic")
        return await self.discover(niche, limit, mode)
    
    def to_opportunities(self, result: OpportunityResult) -> List[Opportunity]:
        """Convert OpportunityResult to list of Opportunity models.
        
        Args:
            result: OpportunityResult object
            
        Returns:
            List of Opportunity objects
        """
        opportunities = []
        for topic in result.ranked_topics:
            opp = Opportunity(
                topic=topic.title,
                niche=topic.niche,
                trend_score=topic.trend_score,
                demand_score=topic.demand_score,
                competition_score=1.0 - topic.feasibility_score,
                opportunity_score=topic.opportunity_score,
                description=topic.description,
                keywords=topic.keywords,
                metadata={
                    "format": topic.format_recommendation,
                    "effort": topic.estimated_effort,
                    "reach": topic.potential_reach,
                },
            )
            opportunities.append(opp)
        return opportunities
