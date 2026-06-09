"""Curiosity Engine for creating and analyzing curiosity gaps."""

from dataclasses import dataclass, field
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


@dataclass
class CuriosityAnalysis:
    """Curiosity analysis result."""
    
    curiosity_score: float  # 0-100
    open_loops: int
    curiosity_gaps: List[str] = field(default_factory=list)
    tension_points: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    curiosity_triggers: List[str] = field(default_factory=list)


class CuriosityEngine:
    """Creates and analyzes curiosity elements in content."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Curiosity trigger patterns
        self.curiosity_patterns = [
            "but here's the thing", "however", "what most people don't know",
            "the truth is", "actually", "surprisingly", "here's the catch",
            "there's a problem", "but wait", "here's where it gets interesting",
            "you might be wondering", "the real question is", "what if"
        ]
        
        # Open loop phrases
        self.open_loop_phrases = [
            "coming up", "later we'll see", "in a moment",
            "stick around", "don't go anywhere", "after the break",
            "but first", "before we get to that", "one more thing"
        ]
    
    def analyze(self, script: str) -> CuriosityAnalysis:
        """
        Analyze curiosity elements in a script.
        
        Args:
            script: Video script
            
        Returns:
            CuriosityAnalysis with score and insights
        """
        logger.info("Analyzing curiosity elements")
        
        script_lower = script.lower()
        
        # Count curiosity triggers
        curiosity_triggers = self._find_curiosity_triggers(script_lower)
        
        # Find open loops
        open_loops = self._find_open_loops(script_lower)
        
        # Identify curiosity gaps
        curiosity_gaps = self._identify_curiosity_gaps(script)
        
        # Find tension points
        tension_points = self._find_tension_points(script_lower)
        
        # Calculate curiosity score
        curiosity_score = self._calculate_score(
            len(curiosity_triggers),
            len(open_loops),
            len(curiosity_gaps),
            len(tension_points),
            len(script.split())
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            curiosity_score,
            len(open_loops),
            len(curiosity_gaps)
        )
        
        return CuriosityAnalysis(
            curiosity_score=round(curiosity_score, 2),
            open_loops=len(open_loops),
            curiosity_gaps=curiosity_gaps,
            tension_points=tension_points,
            recommendations=recommendations,
            curiosity_triggers=curiosity_triggers[:10]
        )
    
    def _find_curiosity_triggers(self, text: str) -> List[str]:
        """Find curiosity trigger phrases in text."""
        triggers = []
        for pattern in self.curiosity_patterns:
            if pattern in text:
                triggers.append(pattern)
        return triggers
    
    def _find_open_loops(self, text: str) -> List[str]:
        """Find open loop phrases in text."""
        loops = []
        for phrase in self.open_loop_phrases:
            if phrase in text:
                loops.append(phrase)
        return loops
    
    def _identify_curiosity_gaps(self, script: str) -> List[str]:
        """Identify specific curiosity gaps in the script."""
        gaps = []
        lines = script.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Look for promise without immediate delivery
            if any(phrase in line_lower for phrase in ["we'll discover", "you'll learn", "i'll show"]):
                if i + 1 < len(lines) and not any(phrase in lines[i+1].lower() for phrase in ["now", "first", "let's"]):
                    gaps.append(f"Promise at line {i+1} - consider delivering sooner")
            
            # Look for questions without immediate answers
            if "?" in line and i + 1 < len(lines) and "?" not in lines[i+1]:
                if len(line.split()) < 15:  # Short question
                    gaps.append(f"Question at line {i+1} creates curiosity gap")
        
        return gaps[:5]
    
    def _find_tension_points(self, text: str) -> List[str]:
        """Find tension-building elements."""
        tension_words = [
            "problem", "challenge", "obstacle", "difficult", "struggle",
            "conflict", "tension", "crisis", "danger", "risk"
        ]
        
        tensions = []
        for word in tension_words:
            if word in text:
                tensions.append(word)
        
        return tensions
    
    def _calculate_score(
        self,
        trigger_count: int,
        open_loop_count: int,
        gap_count: int,
        tension_count: int,
        word_count: int
    ) -> float:
        """Calculate overall curiosity score."""
        # Base score
        score = 50.0
        
        # Triggers (ideal: 1 per 100 words)
        trigger_ratio = trigger_count / (word_count / 100)
        if 0.5 <= trigger_ratio <= 2.0:
            score += 20
        elif trigger_ratio > 0:
            score += 10
        
        # Open loops (ideal: 2-4 per script)
        if 2 <= open_loop_count <= 4:
            score += 20
        elif open_loop_count >= 1:
            score += 10
        
        # Curiosity gaps (ideal: 3-5)
        if 3 <= gap_count <= 5:
            score += 15
        elif gap_count >= 1:
            score += 8
        
        # Tension points (adds engagement)
        score += min(15, tension_count * 3)
        
        return min(100, score)
    
    def _generate_recommendations(
        self,
        curiosity_score: float,
        open_loop_count: int,
        gap_count: int
    ) -> List[str]:
        """Generate recommendations for improving curiosity."""
        recommendations = []
        
        if curiosity_score < 60:
            recommendations.append(
                "Add more curiosity triggers like 'but here's the thing' or 'what most people don't know'"
            )
        
        if open_loop_count < 2:
            recommendations.append(
                "Create 2-3 open loops to keep viewers watching (e.g., 'coming up', 'later we'll see')"
            )
        
        if gap_count < 3:
            recommendations.append(
                "Introduce more curiosity gaps by posing questions before providing answers"
            )
        
        if curiosity_score >= 70:
            recommendations.append(
                "Good curiosity level! Consider adding one more tension point for maximum engagement"
            )
        
        recommendations.append(
            "Use the 'promise → delay → deliver' pattern for key information"
        )
        
        return recommendations[:5]
    
    def create_curiosity_gap(self, topic: str) -> str:
        """Generate a curiosity gap statement for a topic."""
        templates = [
            f"Most people think they understand {topic}, but there's one crucial detail everyone misses...",
            f"What if everything you knew about {topic} was only half the story?",
            f"There's a secret about {topic} that experts don't want you to know...",
            f"The truth about {topic} will shock you - here's what really happens...",
        ]
        
        import random
        return random.choice(templates)
    
    def create_open_loop(self, content_type: str = "general") -> str:
        """Generate an open loop phrase."""
        loops = {
            "general": [
                "But we'll get to that in a moment...",
                "Coming up, I'll reveal something that changes everything...",
                "Stick around, because what comes next is crucial...",
            ],
            "educational": [
                "After we cover this, I'll show you the practical application...",
                "The real breakthrough comes when we combine this with...",
            ],
            "storytelling": [
                "But little did they know, the real challenge was yet to come...",
                "What happened next would change everything...",
            ]
        }
        
        import random
        options = loops.get(content_type, loops["general"])
        return random.choice(options)
