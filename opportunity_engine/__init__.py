"""YT Auto Opportunity Engine Module."""

from .trend_scanner import TrendScanner
from .demand_validator import DemandValidator
from .niche_gap_finder import NicheGapFinder
from .topic_ranker import TopicRanker
from .engine import OpportunityEngine, OpportunityResult, EnhancedRankedTopic
from .niche_intelligence import NicheIntelligence, NicheAnalysis, NicheProfile, AudienceType

__all__ = [
    "TrendScanner",
    "DemandValidator",
    "NicheGapFinder",
    "TopicRanker",
    "OpportunityEngine",
    "OpportunityResult",
    "EnhancedRankedTopic",
    "NicheIntelligence",
    "NicheAnalysis",
    "NicheProfile",
    "AudienceType",
]
