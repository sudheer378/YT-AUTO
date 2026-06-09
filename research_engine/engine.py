"""
Research Engine - Topic Research and Fact Collection
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ResearchSource:
    """Represents a research source."""
    title: str
    url: str
    source_type: str  # academic, news, official, expert
    credibility_score: float
    publish_date: Optional[str] = None


@dataclass
class ResearchFact:
    """Represents a research fact."""
    fact: str
    category: str  # key_fact, statistic, historical, misconception
    confidence: float
    sources: List[str] = field(default_factory=list)


@dataclass
class ResearchReport:
    """Complete research report for a topic."""
    topic: str
    summary: str
    key_facts: List[ResearchFact] = field(default_factory=list)
    statistics: List[ResearchFact] = field(default_factory=list)
    historical_context: List[ResearchFact] = field(default_factory=list)
    misconceptions: List[ResearchFact] = field(default_factory=list)
    expert_perspectives: List[ResearchFact] = field(default_factory=list)
    references: List[ResearchSource] = field(default_factory=list)
    source_links: List[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "topic": self.topic,
            "summary": self.summary,
            "key_facts": [f.fact for f in self.key_facts],
            "statistics": [f.fact for f in self.statistics],
            "historical_context": [f.fact for f in self.historical_context],
            "misconceptions": [f.fact for f in self.misconceptions],
            "expert_perspectives": [f.fact for f in self.expert_perspectives],
            "references": [{"title": r.title, "url": r.url, "type": r.source_type} for r in self.references],
            "source_links": self.source_links,
            "generated_at": self.generated_at
        }
    
    def to_markdown(self) -> str:
        """Export as markdown."""
        md = f"# Research Report: {self.topic}\n\n"
        md += f"*Generated: {self.generated_at}*\n\n"
        md += f"## Summary\n{self.summary}\n\n"
        
        if self.key_facts:
            md += "## Key Facts\n"
            for i, fact in enumerate(self.key_facts, 1):
                md += f"{i}. {fact.fact} (Confidence: {fact.confidence:.0%})\n"
            md += "\n"
        
        if self.statistics:
            md += "## Statistics\n"
            for stat in self.statistics:
                md += f"- {stat.fact}\n"
            md += "\n"
        
        if self.historical_context:
            md += "## Historical Context\n"
            for hist in self.historical_context:
                md += f"- {hist.fact}\n"
            md += "\n"
        
        if self.misconceptions:
            md += "## Common Misconceptions\n"
            for mis in self.misconceptions:
                md += f"- ❌ {mis.fact}\n"
            md += "\n"
        
        if self.references:
            md += "## References\n"
            for ref in self.references:
                md += f"- [{ref.title}]({ref.url}) - {ref.source_type}\n"
        
        return md
    
    def to_json(self) -> Dict:
        """Export as JSON-compatible dict."""
        return self.to_dict()


class ResearchEngine:
    """Engine for generating research reports."""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        logger.info("ResearchEngine initialized")
    
    async def generate(self, topic: str, niche: str = "general") -> ResearchReport:
        """Generate a complete research report."""
        logger.info(f"Generating research report for: {topic}")
        
        try:
            # Mock implementation - would use AI client in production
            report = self._generate_mock_report(topic, niche)
            logger.info(f"Research report generated with {len(report.key_facts)} facts")
            return report
        except Exception as e:
            logger.error(f"Error generating research report: {e}")
            raise
    
    def _generate_mock_report(self, topic: str, niche: str) -> ResearchReport:
        """Generate mock research report."""
        return ResearchReport(
            topic=topic,
            summary=f"Comprehensive research analysis of '{topic}' covering key facts, statistics, historical context, and expert perspectives.",
            key_facts=[
                ResearchFact(fact="Key insight about {topic} that viewers should know", category="key_fact", confidence=0.95),
                ResearchFact(fact="Important finding related to {topic}", category="key_fact", confidence=0.90),
                ResearchFact(fact="Critical understanding of {topic}", category="key_fact", confidence=0.88),
            ],
            statistics=[
                ResearchFact(fact="78% of experts agree on this {topic} statistic", category="statistic", confidence=0.92),
                ResearchFact(fact="Growth rate of 45% year-over-year in {topic} sector", category="statistic", confidence=0.89),
            ],
            historical_context=[
                ResearchFact(fact="{topic} has evolved significantly since its inception", category="historical", confidence=0.85),
            ],
            misconceptions=[
                ResearchFact(fact="Common myth about {topic} that needs clarification", category="misconception", confidence=0.91),
            ],
            expert_perspectives=[
                ResearchFact(fact="Leading researchers emphasize this aspect of {topic}", category="expert", confidence=0.87),
            ],
            references=[
                ResearchSource(title=f"Academic Study on {topic}", url="https://example.com/study", source_type="academic", credibility_score=0.95),
                ResearchSource(title=f"Industry Report: {topic}", url="https://example.com/report", source_type="official", credibility_score=0.90),
            ],
            source_links=["https://example.com/source1", "https://example.com/source2"]
        )


__all__ = ["ResearchEngine", "ResearchReport", "ResearchFact", "ResearchSource"]
