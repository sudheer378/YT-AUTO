"""Watch Time Optimizer for maximizing audience retention."""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class WatchTimeOptimization:
    """Watch time optimization recommendations."""
    
    current_estimated_retention: float  # Percentage
    optimized_estimated_retention: float  # Percentage
    improvement_potential: float  # Percentage points
    structural_issues: List[str] = field(default_factory=list)
    pacing_recommendations: List[str] = field(default_factory=list)
    engagement_boosters: List[str] = field(default_factory=list)
    optimal_video_length: int = 0  # seconds
    key_moments: List[Dict] = field(default_factory=list)


class WatchTimeOptimizer:
    """Optimizes content for maximum watch time and retention."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Retention benchmarks by format
        self.retention_benchmarks = {
            "documentary": 0.55,
            "explainer": 0.50,
            "tutorial": 0.45,
            "storytelling": 0.60,
            "news": 0.40,
            "entertainment": 0.45,
            "review": 0.50,
            "general": 0.48,
        }
        
        # Optimal segment lengths (seconds)
        self.segment_lengths = {
            "hook": 30,
            "intro": 60,
            "main_content": 180,
            "transition": 15,
            "cta": 30,
        }
    
    def optimize(
        self,
        script: str,
        format_type: str = "general",
        target_length_seconds: int = 600
    ) -> WatchTimeOptimization:
        """
        Analyze and optimize script for watch time.
        
        Args:
            script: Video script
            format_type: Content format
            target_length_seconds: Target video length
            
        Returns:
            WatchTimeOptimization with recommendations
        """
        logger.info(f"Optimizing for watch time ({format_type}, {target_length_seconds}s)")
        
        # Estimate current retention
        current_retention = self._estimate_current_retention(script, format_type)
        
        # Identify structural issues
        structural_issues = self._identify_structural_issues(script, format_type)
        
        # Generate pacing recommendations
        pacing_recommendations = self._generate_pacing_recommendations(
            script, target_length_seconds
        )
        
        # Suggest engagement boosters
        engagement_boosters = self._suggest_engagement_boosters(script)
        
        # Calculate optimized retention potential
        improvement = self._calculate_improvement_potential(
            len(structural_issues),
            len(pacing_recommendations),
            len(engagement_boosters)
        )
        
        optimized_retention = min(0.75, current_retention + improvement)
        
        # Determine optimal video length
        optimal_length = self._determine_optimal_length(script, format_type)
        
        # Identify key moments to structure
        key_moments = self._identify_key_moments(script, optimal_length)
        
        return WatchTimeOptimization(
            current_estimated_retention=round(current_retention * 100, 2),
            optimized_estimated_retention=round(optimized_retention * 100, 2),
            improvement_potential=round(improvement * 100, 2),
            structural_issues=structural_issues,
            pacing_recommendations=pacing_recommendations,
            engagement_boosters=engagement_boosters,
            optimal_video_length=optimal_length,
            key_moments=key_moments
        )
    
    def _estimate_current_retention(self, script: str, format_type: str) -> float:
        """Estimate current retention based on script quality."""
        base_retention = self.retention_benchmarks.get(
            format_type.lower(),
            self.retention_benchmarks["general"]
        )
        
        # Adjust for script characteristics
        words = script.split()
        word_count = len(words)
        
        # Check for hook quality
        first_50_words = " ".join(words[:50]).lower()
        hook_quality = 1.0
        if any(trigger in first_50_words for trigger in ["what if", "imagine", "secret", "truth"]):
            hook_quality = 1.15
        
        # Check for structure
        structure_words = ["first", "next", "then", "finally", "conclusion"]
        structure_count = sum(1 for word in structure_words if word in script.lower())
        structure_factor = 1.0 + (min(structure_count, 5) * 0.02)
        
        # Check for engagement elements
        engagement_words = ["you", "your", "we", "let's", "imagine"]
        engagement_count = sum(1 for word in engagement_words if word in script.lower())
        engagement_factor = 1.0 + (min(engagement_count / 20, 0.1))
        
        estimated_retention = base_retention * hook_quality * structure_factor * engagement_factor
        
        return min(0.70, estimated_retention)
    
    def _identify_structural_issues(self, script: str, format_type: str) -> List[str]:
        """Identify structural problems affecting retention."""
        issues = []
        lines = script.split('\n')
        words = script.split()
        
        # Check for missing hook
        first_50 = " ".join(words[:50]).lower()
        if any(greeting in first_50 for greeting in ["hello", "welcome", "hi everyone"]):
            issues.append("Weak opening - starts with greeting instead of hook")
        
        # Check for clear sections
        section_markers = ["first", "second", "third", "next", "finally"]
        has_sections = any(marker in script.lower() for marker in section_markers)
        if not has_sections and len(words) > 500:
            issues.append("Long content without clear section breaks")
        
        # Check for CTA placement
        cta_words = ["subscribe", "like", "comment", "share"]
        cta_present = any(word in script.lower() for word in cta_words)
        if not cta_present:
            issues.append("Missing call-to-action")
        
        # Check conclusion
        last_100 = " ".join(words[-100:]).lower() if len(words) > 100 else script.lower()
        conclusion_markers = ["conclusion", "summary", "to wrap up", "thanks for watching"]
        if not any(marker in last_100 for marker in conclusion_markers):
            issues.append("No clear conclusion or wrap-up")
        
        # Check paragraph density
        if len(lines) < 5 and len(words) > 300:
            issues.append("Dense text without visual breaks - consider adding sections")
        
        return issues
    
    def _generate_pacing_recommendations(
        self,
        script: str,
        target_length: int
    ) -> List[str]:
        """Generate pacing recommendations."""
        recommendations = []
        words = script.split()
        word_count = len(words)
        
        # Calculate current WPM estimate
        estimated_wpm = (word_count / target_length) * 60
        
        if estimated_wpm < 130:
            recommendations.append(
                "Pace is slow - consider trimming or speaking faster (target: 140-160 WPM)"
            )
        elif estimated_wpm > 170:
            recommendations.append(
                "Pace is very fast - add pauses for key points to improve comprehension"
            )
        else:
            recommendations.append(
                "Good pace - maintain 140-160 WPM for optimal engagement"
            )
        
        # Pattern interrupt recommendation
        if word_count > 800:
            recommendations.append(
                "Add pattern interrupts every 2-3 minutes (visual change, question, story)"
            )
        
        # Hook timing
        recommendations.append(
            "Deliver main value proposition within first 15 seconds"
        )
        
        # Mid-point engagement
        recommendations.append(
                "Add engagement element at 50% mark to prevent drop-off"
        )
        
        return recommendations
    
    def _suggest_engagement_boosters(self, script: str) -> List[str]:
        """Suggest elements to boost engagement."""
        boosters = []
        script_lower = script.lower()
        
        # Check for questions
        question_count = script.count("?")
        if question_count < 3:
            boosters.append("Add more direct questions to viewer throughout")
        
        # Check for stories
        story_words = ["story", "once", "happened", "experience", "journey"]
        if not any(word in script_lower for word in story_words):
            boosters.append("Include a relevant story or case study")
        
        # Check for examples
        example_words = ["for example", "such as", "like when", "imagine"]
        if not any(word in script_lower for word in example_words):
            boosters.append("Add concrete examples to illustrate abstract concepts")
        
        # Check for visual cues
        visual_words = ["look", "see", "watch", "notice", "observe"]
        if not any(word in script_lower for word in visual_words):
            boosters.append("Add visual direction cues for editor")
        
        # Surprise element
        surprise_words = ["surprising", "shocking", "unexpected", "amazing"]
        if not any(word in script_lower for word in surprise_words):
            boosters.append("Include at least one surprising fact or revelation")
        
        return boosters[:5]
    
    def _calculate_improvement_potential(
        self,
        issue_count: int,
        pacing_count: int,
        booster_count: int
    ) -> float:
        """Calculate potential retention improvement."""
        # Each fix can improve retention by ~2-5%
        base_improvement = 0.02
        
        total_fixes = issue_count + pacing_count + booster_count
        improvement = base_improvement * total_fixes
        
        # Cap at realistic maximum
        return min(0.20, improvement)
    
    def _determine_optimal_length(self, script: str, format_type: str) -> int:
        """Determine optimal video length for the content."""
        word_count = len(script.split())
        
        # Base WPM assumption
        target_wpm = 150
        
        # Calculate base length
        base_length = (word_count / target_wpm) * 60
        
        # Adjust for format
        format_adjustments = {
            "documentary": 1.2,
            "explainer": 1.0,
            "tutorial": 1.1,
            "storytelling": 1.3,
            "news": 0.8,
            "entertainment": 0.9,
            "review": 1.0,
        }
        
        adjustment = format_adjustments.get(format_type.lower(), 1.0)
        optimal_length = base_length * adjustment
        
        # Round to nearest minute
        return round(optimal_length / 60) * 60
    
    def _identify_key_moments(
        self,
        script: str,
        video_length: int
    ) -> List[Dict]:
        """Identify key moments for structuring the video."""
        moments = []
        words = script.split()
        total_words = len(words)
        
        # Hook (0-30s)
        hook_words = int(total_words * (30 / video_length))
        moments.append({
            "moment": "Hook",
            "timestamp": "0:00-0:30",
            "purpose": "Grab attention immediately",
            "word_range": f"1-{hook_words}"
        })
        
        # Intro (30-60s)
        intro_words = int(total_words * (60 / video_length))
        moments.append({
            "moment": "Intro/Setup",
            "timestamp": "0:30-1:00",
            "purpose": "Set expectations and context",
            "word_range": f"{hook_words}-{intro_words}"
        })
        
        # Main content segments
        segments = 3 if video_length < 600 else 4
        segment_length = (video_length - 120) // segments
        
        for i in range(segments):
            start_time = 60 + (i * segment_length)
            end_time = start_time + segment_length
            moments.append({
                "moment": f"Main Point {i+1}",
                "timestamp": f"{start_time//60}:{start_time%60:02d}-{end_time//60}:{end_time%60:02d}",
                "purpose": "Deliver key content",
                "note": "Add pattern interrupt at end"
            })
        
        # Conclusion
        moments.append({
            "moment": "Conclusion/CTA",
            "timestamp": f"{(video_length-60)//60}:{(video_length-60)%60:02d}-end",
            "purpose": "Summarize and call-to-action",
        })
        
        return moments
