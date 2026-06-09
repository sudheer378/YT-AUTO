"""Hook Analyzer for video retention optimization."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class HookAnalysis:
    """Hook analysis result."""
    
    hook_score: float  # 0-100
    strength_rating: str  # "Excellent", "Good", "Fair", "Weak"
    curiosity_level: float
    emotional_pull: float
    clarity_score: float
    first_30_words: str = ""
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    improved_hook: str = ""


class HookAnalyzer:
    """Analyzes and scores video hooks for retention potential."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Hook patterns that work well
        self.strong_openings = [
            "what if", "imagine", "have you ever", "did you know",
            "the truth about", "nobody tells you", "secret", "revealed",
            "i'm going to show you", "you're about to discover",
            "this will change", "the real reason", "actually"
        ]
        
        # Weak opening patterns
        self.weak_openings = [
            "hello everyone", "welcome back", "in this video",
            "today we're going to", "let's talk about", "so",
            "um", "uh", "hey guys"
        ]
    
    def analyze(self, script: str, title: str = "") -> HookAnalysis:
        """
        Analyze the hook of a video script.
        
        Args:
            script: Full video script
            title: Video title (optional)
            
        Returns:
            HookAnalysis with score and recommendations
        """
        logger.info("Analyzing video hook")
        
        # Extract first 30-50 words as hook
        words = script.split()
        first_30_words = " ".join(words[:30])
        first_50_words = " ".join(words[:50])
        
        # Calculate component scores
        curiosity_score = self._analyze_curiosity(first_50_words)
        emotional_score = self._analyze_emotional_pull(first_50_words)
        clarity_score = self._analyze_clarity(first_50_words)
        pattern_score = self._analyze_opening_patterns(first_30_words)
        
        # Calculate overall hook score
        hook_score = (
            curiosity_score * 0.35 +
            emotional_score * 0.30 +
            clarity_score * 0.20 +
            pattern_score * 0.15
        )
        
        # Clamp to 0-100
        hook_score = max(0, min(100, hook_score))
        
        # Determine strength rating
        if hook_score >= 85:
            strength_rating = "Excellent"
        elif hook_score >= 70:
            strength_rating = "Good"
        elif hook_score >= 55:
            strength_rating = "Fair"
        else:
            strength_rating = "Weak"
        
        # Identify issues
        issues = self._identify_issues(first_50_words, hook_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            first_50_words, hook_score, issues
        )
        
        # Generate improved hook suggestion
        improved_hook = self._suggest_improvement(
            first_50_words, title, recommendations
        )
        
        return HookAnalysis(
            hook_score=round(hook_score, 2),
            strength_rating=strength_rating,
            curiosity_level=round(curiosity_score, 2),
            emotional_pull=round(emotional_score, 2),
            clarity_score=round(clarity_score, 2),
            first_30_words=first_30_words,
            issues=issues,
            recommendations=recommendations,
            improved_hook=improved_hook
        )
    
    def _analyze_curiosity(self, text: str) -> float:
        """Analyze curiosity level in hook."""
        text_lower = text.lower()
        score = 50.0
        
        # Check for strong curiosity triggers
        curiosity_triggers = [
            "secret", "truth", "revealed", "nobody knows",
            "what if", "imagine", "discover", "shocking",
            "surprising", "unexpected", "actually", "really"
        ]
        
        trigger_count = sum(1 for trigger in curiosity_triggers if trigger in text_lower)
        score += min(30, trigger_count * 10)
        
        # Check for questions
        if "?" in text:
            score += 10
        
        # Check for incomplete information (creates curiosity gap)
        if "..." in text or "but" in text_lower or "however" in text_lower:
            score += 10
        
        return min(100, score)
    
    def _analyze_emotional_pull(self, text: str) -> float:
        """Analyze emotional engagement in hook."""
        text_lower = text.lower()
        score = 50.0
        
        # Emotional words
        positive_emotions = [
            "amazing", "incredible", "awesome", "exciting", "fantastic",
            "brilliant", "perfect", "wonderful", "love"
        ]
        negative_emotions = [
            "terrible", "awful", "horrible", "frustrating", "scary",
            "shocking", "disturbing", "worst", "hate"
        ]
        urgency_words = [
            "now", "immediately", "urgent", "critical", "must",
            "before it's too late", "right now"
        ]
        
        pos_count = sum(1 for word in positive_emotions if word in text_lower)
        neg_count = sum(1 for word in negative_emotions if word in text_lower)
        urg_count = sum(1 for word in urgency_words if word in text_lower)
        
        score += min(25, (pos_count + neg_count) * 8)
        score += min(15, urg_count * 10)
        
        # Direct address increases emotional connection
        if "you" in text_lower or "your" in text_lower:
            score += 10
        
        return min(100, score)
    
    def _analyze_clarity(self, text: str) -> float:
        """Analyze clarity of the hook."""
        text_lower = text.lower()
        score = 70.0
        
        # Penalize filler words at start
        fillers = ["um", "uh", "so", "well", "like"]
        if any(text_lower.startswith(filler) for filler in fillers):
            score -= 20
        
        # Reward clear value proposition
        value_indicators = [
            "you'll learn", "i'll show", "we'll cover",
            "by the end", "after this", "discover how"
        ]
        if any(indicator in text_lower for indicator in value_indicators):
            score += 20
        
        # Simple language is clearer
        avg_word_length = sum(len(word) for word in text.split()) / max(1, len(text.split()))
        if avg_word_length < 5:
            score += 10
        elif avg_word_length > 7:
            score -= 10
        
        return max(0, min(100, score))
    
    def _analyze_opening_patterns(self, text: str) -> float:
        """Analyze opening pattern effectiveness."""
        text_lower = text.lower().strip()
        
        # Check for strong openings
        for pattern in self.strong_openings:
            if text_lower.startswith(pattern) or pattern in text_lower[:30]:
                return 90.0
        
        # Check for weak openings
        for pattern in self.weak_openings:
            if text_lower.startswith(pattern):
                return 40.0
        
        return 65.0
    
    def _identify_issues(self, text: str, hook_score: float) -> List[str]:
        """Identify specific issues with the hook."""
        issues = []
        text_lower = text.lower()
        
        if hook_score < 60:
            # Generic greeting
            if any(text_lower.startswith(greeting) for greeting in ["hello", "hi", "hey", "welcome"]):
                issues.append("Starts with generic greeting instead of compelling hook")
            
            # No clear value proposition
            if not any(indicator in text_lower for indicator in ["learn", "discover", "show", "reveal"]):
                issues.append("Missing clear value proposition")
            
            # Too slow to get to point
            if len(text.split()) > 40 and "?" not in text:
                issues.append("Hook is too long - get to the point faster")
        
        # Filler words
        if text_lower.startswith(("um", "uh", "so ", "well ")) :
            issues.append("Contains filler words at the start")
        
        # No curiosity element
        curiosity_words = ["what", "why", "how", "secret", "truth", "reveal"]
        if not any(word in text_lower for word in curiosity_words):
            issues.append("Lacks curiosity-inducing elements")
        
        return issues
    
    def _generate_recommendations(
        self,
        text: str,
        hook_score: float,
        issues: List[str]
    ) -> List[str]:
        """Generate specific recommendations for improvement."""
        recommendations = []
        
        if hook_score < 70:
            recommendations.append(
                "Start with a bold statement, surprising fact, or provocative question"
            )
        
        if "curiosity" in str(issues).lower():
            recommendations.append(
                "Create a curiosity gap - tease what viewers will discover"
            )
        
        if "value" in str(issues).lower():
            recommendations.append(
                "Clearly state what viewers will gain by watching"
            )
        
        if "filler" in str(issues).lower():
            recommendations.append(
                "Remove filler words and get straight to the hook"
            )
        
        if len(text.split()) > 40:
            recommendations.append(
                "Shorten hook to 15-25 words for maximum impact"
            )
        
        recommendations.append(
            "Use 'you' language to speak directly to the viewer"
        )
        
        return recommendations[:5]
    
    def _suggest_improvement(
        self,
        original_hook: str,
        title: str,
        recommendations: List[str]
    ) -> str:
        """Generate an improved hook suggestion."""
        # This is a simplified suggestion - in production, this would use AI
        suggestions = []
        
        if title:
            suggestions.append(
                f"What if everything you knew about {title} was wrong? "
                f"In this video, I'll reveal the truth..."
            )
        else:
            suggestions.append(
                "Here's something most people don't know... "
                "By the end of this video, you'll understand exactly..."
            )
        
        suggestions.append(
            "Imagine discovering [benefit] in just [timeframe]. "
            "That's exactly what we're doing today..."
        )
        
        return suggestions[0]
