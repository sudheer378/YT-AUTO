"""Quality Evaluator - Evaluates content quality and safety."""

from typing import List, Dict, Any, Optional
import logging
import re

from core.base_engine import BaseEngine
from utils.logger import get_logger
from config.models import QualityMetrics, Script, ContentFormat
from config.settings import get_settings


logger = get_logger(__name__)


class QualityEvaluator(BaseEngine):
    """Evaluates content for quality, safety, and monetization potential."""
    
    def __init__(self):
        super().__init__("quality_evaluator")
        self._safety_keywords = {
            "violence": ["kill", "death", "blood", "fight", "attack", "weapon"],
            "adult": ["nude", "sex", "explicit", "adult", "xxx"],
            "hate": ["hate", "racist", "discrimination", "supremacy"],
            "dangerous": ["dangerous", "stunt", "challenge", "risky"],
            "misinformation": ["conspiracy", "fake news", "hoax", "false"],
        }
        self._monetization_keywords = {
            "positive": ["tutorial", "guide", "review", "analysis", "educational", "tips"],
            "negative": ["clickbait", "shocking", "you won't believe", "crazy"],
        }
    
    async def evaluate(
        self,
        script: Script,
        topic: str,
        niche: str = "general",
    ) -> QualityMetrics:
        """Evaluate content quality.
        
        Args:
            script: Video script to evaluate
            topic: Video topic
            niche: Content niche
            
        Returns:
            QualityMetrics object
        """
        try:
            self.logger.info(f"Evaluating quality for: {topic}")
            
            # Calculate individual scores
            originality = await self._calculate_originality(script)
            monetization = await self._calculate_monetization_score(script, topic)
            safety = await self._calculate_safety_score(script)
            source_validation = await self._validate_sources(script)
            value_add = await self._calculate_value_add(script, niche)
            
            # Calculate final score
            final_score = (
                0.2 * originality +
                0.25 * monetization +
                0.25 * safety +
                0.15 * source_validation +
                0.15 * value_add
            )
            
            # Generate issues and recommendations
            issues = []
            recommendations = []
            
            if safety < 0.7:
                issues.append("Content may contain sensitive topics")
                recommendations.append("Review content for policy compliance")
            
            if monetization < 0.6:
                issues.append("Low monetization potential detected")
                recommendations.append("Add more educational or value-driven content")
            
            if originality < 0.6:
                issues.append("Content may lack originality")
                recommendations.append("Add unique perspectives or analysis")
            
            if value_add < 0.6:
                issues.append("Limited value addition detected")
                recommendations.append("Include actionable insights or takeaways")
            
            return QualityMetrics(
                originality_score=originality,
                monetization_score=monetization,
                safety_score=safety,
                source_validation_score=source_validation,
                value_add_score=value_add,
                final_content_score=final_score,
                issues=issues,
                recommendations=recommendations,
            )
            
        except Exception as e:
            self.logger.error(f"Error evaluating quality: {e}")
            return self._fallback_metrics()
    
    async def _calculate_originality(self, script: Script) -> float:
        """Calculate originality score.
        
        Args:
            script: Video script
            
        Returns:
            Originality score (0-1)
        """
        # TODO: Implement actual plagiarism detection
        content = " ".join(s.content for s in script.sections)
        
        # Mock calculation based on content characteristics
        word_count = len(content.split())
        unique_words = len(set(content.lower().split()))
        
        # Higher unique word ratio suggests more original content
        uniqueness_ratio = unique_words / word_count if word_count > 0 else 0
        
        # Bonus for longer, more detailed content
        length_bonus = min(0.2, word_count / 5000)
        
        base_score = 0.5 + (uniqueness_ratio * 0.3) + length_bonus
        return min(1.0, base_score)
    
    async def _calculate_monetization_score(
        self,
        script: Script,
        topic: str,
    ) -> float:
        """Calculate monetization potential score.
        
        Args:
            script: Video script
            topic: Video topic
            
        Returns:
            Monetization score (0-1)
        """
        content = " ".join(s.content for s in script.sections).lower()
        topic_lower = topic.lower()
        
        score = 0.5  # Base score
        
        # Check for positive monetization keywords
        for keyword in self._monetization_keywords["positive"]:
            if keyword in content or keyword in topic_lower:
                score += 0.05
        
        # Check for negative monetization keywords
        for keyword in self._monetization_keywords["negative"]:
            if keyword in content or keyword in topic_lower:
                score -= 0.1
        
        # Educational content tends to monetize better
        if any(fmt in script.format for fmt in ["documentary", "explainer", "tutorial"]):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    async def _calculate_safety_score(self, script: Script) -> float:
        """Calculate safety score.
        
        Args:
            script: Video script
            
        Returns:
            Safety score (0-1)
        """
        content = " ".join(s.content for s in script.sections).lower()
        
        violations = 0
        total_checks = 0
        
        for category, keywords in self._safety_keywords.items():
            total_checks += 1
            for keyword in keywords:
                if keyword in content:
                    violations += 1
                    break  # One violation per category
        
        # Calculate score based on violations
        if violations == 0:
            return 1.0
        elif violations <= 2:
            return 0.8
        elif violations <= 4:
            return 0.5
        else:
            return 0.2
    
    async def _validate_sources(self, script: Script) -> float:
        """Validate sources in content.
        
        Args:
            script: Video script
            
        Returns:
            Source validation score (0-1)
        """
        content = " ".join(s.content for s in script.sections)
        
        # Check for source indicators
        source_indicators = [
            "according to",
            "research shows",
            "study found",
            "experts say",
            "data suggests",
            "source:",
            "reference",
            "citation",
        ]
        
        found_sources = sum(1 for indicator in source_indicators if indicator.lower() in content.lower())
        
        # Score based on number of source references
        if found_sources >= 5:
            return 1.0
        elif found_sources >= 3:
            return 0.8
        elif found_sources >= 1:
            return 0.6
        else:
            return 0.4  # Base score even without explicit sources
    
    async def _calculate_value_add(self, script: Script, niche: str) -> float:
        """Calculate value-add score.
        
        Args:
            script: Video script
            niche: Content niche
            
        Returns:
            Value-add score (0-1)
        """
        content = " ".join(s.content for s in script.sections).lower()
        
        value_indicators = [
            "learn",
            "understand",
            "discover",
            "tips",
            "how to",
            "guide",
            "steps",
            "key takeaway",
            "important",
            "remember",
        ]
        
        found_indicators = sum(1 for indicator in value_indicators if indicator in content)
        
        # Check for actionable content
        has_cta = any(s.section_type == "cta" for s in script.sections)
        has_summary = "summary" in content or "conclusion" in content or "recap" in content
        
        score = 0.3  # Base score
        score += min(0.4, found_indicators * 0.05)
        
        if has_cta:
            score += 0.15
        if has_summary:
            score += 0.15
        
        return min(1.0, score)
    
    def _fallback_metrics(self) -> QualityMetrics:
        """Generate fallback metrics on error."""
        return QualityMetrics(
            originality_score=0.5,
            monetization_score=0.5,
            safety_score=0.8,
            source_validation_score=0.5,
            value_add_score=0.5,
            final_content_score=0.55,
            issues=["Evaluation failed, using default scores"],
            recommendations=["Manual review recommended"],
        )
    
    async def is_safe_for_monetization(self, metrics: QualityMetrics) -> bool:
        """Check if content is safe for monetization.
        
        Args:
            metrics: QualityMetrics object
            
        Returns:
            True if safe for monetization
        """
        settings = get_settings()
        thresholds = settings.quality_thresholds
        
        return (
            metrics.safety_score >= thresholds.min_safety_score and
            metrics.monetization_score >= thresholds.min_monetization_score and
            metrics.final_content_score >= thresholds.min_final_content_score
        )
    
    async def process(self, *args, **kwargs) -> QualityMetrics:
        """Process quality evaluation request."""
        script = kwargs.get("script")
        topic = kwargs.get("topic", "Untitled")
        niche = kwargs.get("niche", "general")
        
        if not script:
            return self._fallback_metrics()
        
        return await self.evaluate(script, topic, niche)
