"""
Channel Auditor - Analyze YouTube channels for growth potential.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ChannelAuditResult:
    """Results from channel audit."""
    channel_name: str
    niche_detected: str
    content_consistency_score: float  # 0-100
    upload_frequency: str  # daily, weekly, monthly, irregular
    topic_diversity_score: float  # 0-100
    growth_potential_score: float  # 0-100
    monetization_potential_score: float  # 0-100
    opportunity_gaps: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    health_score: float = 0.0  # 0-100 overall
    audited_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        """Calculate health score after initialization."""
        if self.health_score == 0.0:
            self.health_score = (
                self.content_consistency_score * 0.25 +
                self.growth_potential_score * 0.30 +
                self.monetization_potential_score * 0.25 +
                (100 - self.topic_diversity_score) * 0.20  # Lower diversity can be good for niche focus
            )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "channel_name": self.channel_name,
            "niche_detected": self.niche_detected,
            "content_consistency_score": self.content_consistency_score,
            "upload_frequency": self.upload_frequency,
            "topic_diversity_score": self.topic_diversity_score,
            "growth_potential_score": self.growth_potential_score,
            "monetization_potential_score": self.monetization_potential_score,
            "opportunity_gaps": self.opportunity_gaps,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations,
            "health_score": self.health_score,
            "audited_at": self.audited_at
        }
    
    def to_markdown(self) -> str:
        """Export as markdown."""
        md = f"# Channel Audit: {self.channel_name}\n\n"
        md += f"*Audited: {self.audited_at}*\n\n"
        md += f"## Health Score: {self.health_score:.1f}/100\n\n"
        md += f"**Niche:** {self.niche_detected}\n\n"
        md += f"**Upload Frequency:** {self.upload_frequency}\n\n"
        
        md += "## Metrics\n"
        md += f"- Content Consistency: {self.content_consistency_score:.1f}/100\n"
        md += f"- Topic Diversity: {self.topic_diversity_score:.1f}/100\n"
        md += f"- Growth Potential: {self.growth_potential_score:.1f}/100\n"
        md += f"- Monetization Potential: {self.monetization_potential_score:.1f}/100\n\n"
        
        if self.strengths:
            md += "## Strengths\n"
            for s in self.strengths:
                md += f"✅ {s}\n"
            md += "\n"
        
        if self.weaknesses:
            md += "## Weaknesses\n"
            for w in self.weaknesses:
                md += f"⚠️ {w}\n"
            md += "\n"
        
        if self.opportunity_gaps:
            md += "## Opportunity Gaps\n"
            for g in self.opportunity_gaps:
                md += f"💡 {g}\n"
            md += "\n"
        
        if self.recommendations:
            md += "## Recommendations\n"
            for r in self.recommendations:
                md += f"📌 {r}\n"
        
        return md
    
    def to_json(self) -> Dict:
        """Export as JSON-compatible dict."""
        return self.to_dict()


class ChannelAuditor:
    """Audit YouTube channels for growth potential."""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        logger.info("ChannelAuditor initialized")
    
    async def audit(self, channel_name: str) -> ChannelAuditResult:
        """Perform channel audit."""
        logger.info(f"Auditing channel: {channel_name}")
        
        try:
            result = self._generate_mock_audit(channel_name)
            logger.info(f"Channel audit complete. Health score: {result.health_score:.1f}")
            return result
        except Exception as e:
            logger.error(f"Error auditing channel: {e}")
            raise
    
    def _generate_mock_audit(self, channel_name: str) -> ChannelAuditResult:
        """Generate mock channel audit."""
        return ChannelAuditResult(
            channel_name=channel_name,
            niche_detected="Educational Content",
            content_consistency_score=75.0,
            upload_frequency="weekly",
            topic_diversity_score=60.0,
            growth_potential_score=82.0,
            monetization_potential_score=78.0,
            opportunity_gaps=[
                "Short-form content underutilized",
                "Community engagement could be higher",
                "Collaboration opportunities not explored"
            ],
            strengths=[
                "Consistent upload schedule",
                "High production quality",
                "Strong niche focus"
            ],
            weaknesses=[
                "Limited content variety",
                "Thumbnail consistency needs improvement",
                "SEO optimization could be better"
            ],
            recommendations=[
                "Add Shorts to increase reach",
                "Improve thumbnail A/B testing",
                "Engage more with community comments",
                "Optimize video titles for search"
            ]
        )


__all__ = ["ChannelAuditor", "ChannelAuditResult"]
