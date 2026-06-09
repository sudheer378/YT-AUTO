"""Niche Intelligence - Implements niche hierarchy and scoring system."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

from core.base_engine import BaseEngine
from utils.logger import get_logger


logger = get_logger(__name__)


class AudienceType(str, Enum):
    """Audience type enumeration."""
    GENERAL = "general"
    ENTHUSIAST = "enthusiast"
    PROFESSIONAL = "professional"
    HOBBYIST = "hobbyist"
    STUDENT = "student"
    CREATOR = "creator"


@dataclass
class NicheLevel:
    """Represents a level in the niche hierarchy."""
    name: str
    description: str
    parent: Optional[str] = None
    sub_levels: List[str] = field(default_factory=list)


@dataclass
class NicheProfile:
    """Complete niche profile with hierarchy."""
    audience: str
    audience_type: AudienceType
    niche: str
    sub_niche: str
    topic: str
    format_recommendation: str
    
    # Scoring factors
    audience_size_score: float = 0.5
    audience_passion_score: float = 0.5
    content_depth_score: float = 0.5
    repeatability_score: float = 0.5
    monetization_potential_score: float = 0.5
    competition_score: float = 0.5  # Lower is better (less competition)
    trend_growth_score: float = 0.5
    
    # Computed scores
    niche_score: float = 0.0
    
    # Analysis
    why_selected: str = ""
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)
    
    # Metadata
    estimated_videos_possible: int = 0
    avg_video_length: str = "10-15 min"
    posting_frequency: str = "weekly"


@dataclass
class NicheAnalysis:
    """Complete niche analysis result."""
    niche_profile: NicheProfile
    related_niches: List[NicheProfile]
    trending_topics: List[str]
    content_gaps: List[str]
    recommended_formats: List[str]
    success_probability: float


class NicheIntelligence(BaseEngine):
    """Implements niche intelligence layer with hierarchy and scoring."""
    
    def __init__(self):
        super().__init__("niche_intelligence")
        
        # Niche hierarchy database (mock - would be expanded in production)
        self.niche_database = {
            "technology": {
                "audience": "Tech enthusiasts and professionals",
                "audience_type": AudienceType.PROFESSIONAL,
                "sub_niches": [
                    "AI & Machine Learning",
                    "Cybersecurity",
                    "Web3 & Blockchain",
                    "Cloud Computing",
                    "IoT & Smart Devices",
                    "Software Development",
                    "Consumer Electronics",
                ],
                "monetization": 0.8,
                "competition": 0.7,
                "trend_growth": 0.9,
            },
            "health_fitness": {
                "audience": "Health-conscious individuals",
                "audience_type": AudienceType.HOBBYIST,
                "sub_niches": [
                    "Mental Health",
                    "Fitness & Workout",
                    "Nutrition & Diet",
                    "Sleep Optimization",
                    "Meditation & Mindfulness",
                    "Weight Loss",
                    "Muscle Building",
                ],
                "monetization": 0.7,
                "competition": 0.6,
                "trend_growth": 0.7,
            },
            "business_finance": {
                "audience": "Entrepreneurs and investors",
                "audience_type": AudienceType.PROFESSIONAL,
                "sub_niches": [
                    "Entrepreneurship",
                    "Digital Marketing",
                    "Personal Finance",
                    "Investing",
                    "E-commerce",
                    "Side Hustles",
                    "Cryptocurrency Trading",
                ],
                "monetization": 0.9,
                "competition": 0.8,
                "trend_growth": 0.6,
            },
            "education": {
                "audience": "Students and lifelong learners",
                "audience_type": AudienceType.STUDENT,
                "sub_niches": [
                    "Science Explained",
                    "History Deep Dives",
                    "Language Learning",
                    "Skill Development",
                    "Career Guidance",
                    "Study Techniques",
                    "Book Summaries",
                ],
                "monetization": 0.5,
                "competition": 0.5,
                "trend_growth": 0.6,
            },
            "entertainment": {
                "audience": "General audience seeking entertainment",
                "audience_type": AudienceType.GENERAL,
                "sub_niches": [
                    "Movie Reviews",
                    "Gaming",
                    "Music Analysis",
                    "Celebrity News",
                    "Comedy Sketches",
                    "Reaction Videos",
                    "Pop Culture",
                ],
                "monetization": 0.6,
                "competition": 0.9,
                "trend_growth": 0.5,
            },
            "lifestyle": {
                "audience": "Lifestyle enthusiasts",
                "audience_type": AudienceType.HOBBYIST,
                "sub_niches": [
                    "Travel Vlogs",
                    "Food & Cooking",
                    "Fashion & Style",
                    "Home Decor",
                    "Minimalism",
                    "Productivity",
                    "Relationships",
                ],
                "monetization": 0.6,
                "competition": 0.7,
                "trend_growth": 0.5,
            },
        }
        
        # Topic examples per sub-niche
        self.topic_examples = {
            "AI & Machine Learning": [
                "How Neural Networks Actually Work",
                "Building Your First AI Model",
                "AI Ethics: The Dark Side of Machine Learning",
                "Top 10 AI Tools for 2024",
            ],
            "Cybersecurity": [
                "Ethical Hacking Basics",
                "How to Protect Your Online Privacy",
                "Biggest Data Breaches of 2024",
                "Cybersecurity Career Guide",
            ],
            "Mental Health": [
                "Understanding Anxiety Disorders",
                "Daily Habits for Better Mental Health",
                "Therapy vs Medication: What Works?",
                "Mindfulness for Beginners",
            ],
            "Entrepreneurship": [
                "From Idea to Startup in 30 Days",
                "Common Startup Mistakes to Avoid",
                "How to Raise Venture Capital",
                "Building a Personal Brand",
            ],
        }
        
        # Format recommendations
        self.format_map = {
            "AI & Machine Learning": "explainer",
            "Cybersecurity": "explainer",
            "Web3 & Blockchain": "explainer",
            "Mental Health": "documentary",
            "Fitness & Workout": "animation",
            "Entrepreneurship": "storytelling",
            "History Deep Dives": "history_documentary",
            "Science Explained": "motion_graphics",
            "True Crime": "crime_documentary",
        }
    
    async def analyze_niche(
        self,
        niche_input: str,
        sub_niche: Optional[str] = None,
        topic: Optional[str] = None,
    ) -> NicheAnalysis:
        """Analyze a niche and generate complete profile.
        
        Args:
            niche_input: Main niche name
            sub_niche: Optional sub-niche specification
            topic: Optional specific topic
            
        Returns:
            NicheAnalysis object
        """
        try:
            self.logger.info(f"Analyzing niche: {niche_input}, sub-niche: {sub_niche}, topic: {topic}")
            
            # Normalize niche input
            niche_key = self._normalize_niche_name(niche_input)
            
            # Get niche data from database or generate synthetic
            niche_data = self.niche_database.get(niche_key, self._generate_synthetic_niche(niche_input))
            
            # Determine sub-niche
            if not sub_niche and niche_data.get("sub_niches"):
                sub_niche = niche_data["sub_niches"][0]  # Default to first
            elif not sub_niche:
                sub_niche = f"{niche_input} Tips"
            
            # Determine topic
            if not topic:
                topic_examples = self.topic_examples.get(sub_niche, [])
                topic = topic_examples[0] if topic_examples else f"Introduction to {sub_niche}"
            
            # Create niche profile
            profile = await self._create_niche_profile(
                niche=niche_input,
                niche_data=niche_data,
                sub_niche=sub_niche,
                topic=topic,
            )
            
            # Find related niches
            related_niches = await self._find_related_niches(niche_key)
            
            # Identify trending topics
            trending_topics = await self._get_trending_topics(sub_niche)
            
            # Find content gaps
            content_gaps = await self._find_content_gaps(sub_niche)
            
            # Recommend formats
            recommended_formats = self._recommend_formats(sub_niche)
            
            # Calculate success probability
            success_prob = self._calculate_success_probability(profile)
            
            return NicheAnalysis(
                niche_profile=profile,
                related_niches=related_niches,
                trending_topics=trending_topics,
                content_gaps=content_gaps,
                recommended_formats=recommended_formats,
                success_probability=success_prob,
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing niche: {e}")
            return self._create_error_analysis(niche_input)
    
    async def _create_niche_profile(
        self,
        niche: str,
        niche_data: Dict[str, Any],
        sub_niche: str,
        topic: str,
    ) -> NicheProfile:
        """Create a complete niche profile with scoring."""
        
        # Calculate individual scores
        audience_size = 0.7  # Mock - would come from real data
        audience_passion = 0.8
        content_depth = 0.6
        repeatability = 0.7
        monetization = niche_data.get("monetization", 0.5)
        competition = niche_data.get("competition", 0.5)
        trend_growth = niche_data.get("trend_growth", 0.5)
        
        # Calculate overall niche score
        niche_score = self._calculate_niche_score(
            audience_size=audience_size,
            audience_passion=audience_passion,
            content_depth=content_depth,
            repeatability=repeatability,
            monetization=monetization,
            competition=competition,
            trend_growth=trend_growth,
        )
        
        # Generate why selected explanation
        why_selected = self._generate_why_selected(
            niche=niche,
            sub_niche=sub_niche,
            niche_score=niche_score,
            trend_growth=trend_growth,
            monetization=monetization,
        )
        
        # Generate SWOT analysis
        strengths, weaknesses, opportunities, threats = self._generate_swot(
            niche_score=niche_score,
            monetization=monetization,
            competition=competition,
            trend_growth=trend_growth,
        )
        
        # Estimate videos possible
        estimated_videos = int(content_depth * repeatability * 100)
        
        # Get audience type
        audience_type = niche_data.get("audience_type", AudienceType.GENERAL)
        
        # Get format recommendation
        format_rec = self.format_map.get(sub_niche, "explainer")
        
        return NicheProfile(
            audience=niche_data.get("audience", "General audience"),
            audience_type=audience_type,
            niche=niche,
            sub_niche=sub_niche,
            topic=topic,
            format_recommendation=format_rec,
            audience_size_score=audience_size,
            audience_passion_score=audience_passion,
            content_depth_score=content_depth,
            repeatability_score=repeatability,
            monetization_potential_score=monetization,
            competition_score=competition,
            trend_growth_score=trend_growth,
            niche_score=niche_score,
            why_selected=why_selected,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            estimated_videos_possible=estimated_videos,
        )
    
    def _calculate_niche_score(
        self,
        audience_size: float,
        audience_passion: float,
        content_depth: float,
        repeatability: float,
        monetization: float,
        competition: float,
        trend_growth: float,
    ) -> float:
        """Calculate overall niche score (0-100).
        
        Formula weights:
        - Audience Size: 15%
        - Audience Passion: 20%
        - Content Depth: 15%
        - Repeatability: 15%
        - Monetization: 20%
        - Competition: 10% (inverted - lower is better)
        - Trend Growth: 5%
        """
        score = (
            0.15 * audience_size +
            0.20 * audience_passion +
            0.15 * content_depth +
            0.15 * repeatability +
            0.20 * monetization +
            0.10 * (1.0 - competition) +  # Invert competition
            0.05 * trend_growth
        )
        
        return round(score * 100, 2)
    
    def _generate_why_selected(
        self,
        niche: str,
        sub_niche: str,
        niche_score: float,
        trend_growth: float,
        monetization: float,
    ) -> str:
        """Generate explanation for why this niche was selected."""
        reasons = []
        
        if niche_score >= 75:
            reasons.append(f"Excellent overall niche score ({niche_score:.1f}/100)")
        elif niche_score >= 60:
            reasons.append(f"Strong niche potential ({niche_score:.1f}/100)")
        else:
            reasons.append(f"Moderate niche opportunity ({niche_score:.1f}/100)")
        
        if trend_growth >= 0.7:
            reasons.append("High growth trend in this space")
        
        if monetization >= 0.7:
            reasons.append("Strong monetization potential")
        
        reasons.append(f"Good fit for '{sub_niche}' content within '{niche}' niche")
        
        return ". ".join(reasons) + "."
    
    def _generate_swot(
        self,
        niche_score: float,
        monetization: float,
        competition: float,
        trend_growth: float,
    ) -> tuple[List[str], List[str], List[str], List[str]]:
        """Generate SWOT analysis for the niche."""
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []
        
        # Strengths
        if niche_score >= 70:
            strengths.append("High overall niche viability")
        if monetization >= 0.7:
            strengths.append("Strong revenue potential")
        if trend_growth >= 0.7:
            strengths.append("Growing market demand")
        
        # Weaknesses
        if monetization < 0.5:
            weaknesses.append("Limited monetization options")
        if niche_score < 50:
            weaknesses.append("Low overall niche score")
        
        # Opportunities
        if competition < 0.5:
            opportunities.append("Low competition allows easier entry")
        if trend_growth >= 0.8:
            opportunities.append("Rapidly expanding audience")
        
        # Threats
        if competition >= 0.7:
            threats.append("High competition may limit growth")
        if trend_growth < 0.4:
            threats.append("Declining or stagnant interest")
        
        # Ensure at least one item in each category
        if not strengths:
            strengths.append("Established audience base")
        if not weaknesses:
            weaknesses.append("Requires consistent content creation")
        if not opportunities:
            opportunities.append("Cross-platform expansion potential")
        if not threats:
            threats.append("Algorithm changes may impact reach")
        
        return strengths, weaknesses, opportunities, threats
    
    def _calculate_success_probability(self, profile: NicheProfile) -> float:
        """Calculate probability of success for this niche."""
        # Weighted formula based on key factors
        probability = (
            0.25 * profile.audience_passion_score +
            0.25 * profile.monetization_potential_score +
            0.20 * profile.trend_growth_score +
            0.15 * profile.repeatability_score +
            0.15 * (1.0 - profile.competition_score)
        )
        
        return round(probability, 3)
    
    async def _find_related_niches(self, niche_key: str) -> List[NicheProfile]:
        """Find related niches."""
        related = []
        
        # Simple mock implementation
        all_keys = list(self.niche_database.keys())
        for key in all_keys[:3]:  # Return up to 3 related
            if key != niche_key:
                data = self.niche_database[key]
                sub_niche = data["sub_niches"][0] if data.get("sub_niches") else "General"
                
                profile = NicheProfile(
                    audience=data.get("audience", "General"),
                    audience_type=data.get("audience_type", AudienceType.GENERAL),
                    niche=key.replace("_", " ").title(),
                    sub_niche=sub_niche,
                    topic=f"Introduction to {sub_niche}",
                    format_recommendation="explainer",
                    niche_score=round((data.get("monetization", 0.5) + data.get("trend_growth", 0.5)) * 50, 2),
                )
                related.append(profile)
        
        return related
    
    async def _get_trending_topics(self, sub_niche: str) -> List[str]:
        """Get trending topics for a sub-niche."""
        # Return from examples or generate synthetic
        return self.topic_examples.get(sub_niche, [
            f"Beginner's Guide to {sub_niche}",
            f"Advanced {sub_niche} Strategies",
            f"{sub_niche} Myths Debunked",
            f"Future of {sub_niche}",
        ])
    
    async def _find_content_gaps(self, sub_niche: str) -> List[str]:
        """Identify content gaps in the sub-niche."""
        # Mock implementation
        return [
            f"Deep dive into {sub_niche} case studies",
            f"Interviews with {sub_niche} experts",
            f"Practical {sub_niche} tutorials",
            f"{sub_niche} tools comparison",
        ]
    
    def _recommend_formats(self, sub_niche: str) -> List[str]:
        """Recommend content formats for the sub-niche."""
        primary = self.format_map.get(sub_niche, "explainer")
        
        all_formats = ["explainer", "documentary", "animation", "storytelling", "shorts"]
        
        # Return primary plus 2 alternatives
        alternatives = [f for f in all_formats if f != primary][:2]
        
        return [primary] + alternatives
    
    def _normalize_niche_name(self, name: str) -> str:
        """Normalize niche name for database lookup."""
        normalized = name.lower().strip()
        normalized = normalized.replace(" ", "_").replace("-", "_")
        
        # Map common variations
        mappings = {
            "tech": "technology",
            "cyber_security": "technology",
            "ai": "technology",
            "health": "health_fitness",
            "fitness": "health_fitness",
            "business": "business_finance",
            "finance": "business_finance",
            "money": "business_finance",
            "learning": "education",
            "edu": "education",
            "entertainment": "entertainment",
            "fun": "entertainment",
            "lifestyle": "lifestyle",
            "life": "lifestyle",
        }
        
        return mappings.get(normalized, normalized)
    
    def _generate_synthetic_niche(self, niche_name: str) -> Dict[str, Any]:
        """Generate synthetic niche data for unknown niches."""
        return {
            "audience": f"{niche_name.title()} enthusiasts",
            "audience_type": AudienceType.ENTHUSIAST,
            "sub_niches": [
                f"{niche_name.title()} Basics",
                f"Advanced {niche_name.title()}",
                f"{niche_name.title()} Trends",
            ],
            "monetization": 0.5,
            "competition": 0.5,
            "trend_growth": 0.5,
        }
    
    def _create_error_analysis(self, niche_input: str) -> NicheAnalysis:
        """Create error analysis result."""
        profile = NicheProfile(
            audience="Unknown",
            audience_type=AudienceType.GENERAL,
            niche=niche_input,
            sub_niche="General",
            topic="Getting Started",
            format_recommendation="explainer",
            niche_score=50.0,
            why_selected="Default profile created due to analysis error.",
        )
        
        return NicheAnalysis(
            niche_profile=profile,
            related_niches=[],
            trending_topics=[],
            content_gaps=[],
            recommended_formats=["explainer"],
            success_probability=0.5,
        )
    
    async def process(self, *args, **kwargs) -> NicheAnalysis:
        """Process niche analysis request."""
        niche_input = kwargs.get("niche", kwargs.get("niche_input", ""))
        sub_niche = kwargs.get("sub_niche")
        topic = kwargs.get("topic")
        return await self.analyze_niche(niche_input, sub_niche, topic)
