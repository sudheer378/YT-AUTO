"""CTR Prediction Engine for YouTube content."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class CTRAnalysis:
    """CTR analysis result."""
    
    predicted_ctr: float  # 0-100
    title_score: float
    thumbnail_score: float
    curiosity_score: float
    emotional_impact: float
    clarity_score: float
    factors: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.85


class CTRPredictor:
    """Predicts Click-Through Rate for YouTube content."""
    
    def __init__(self):
        self.title_factors = {
            "length_optimal": 0.15,
            "curiosity_gap": 0.20,
            "emotional_words": 0.15,
            "numbers_present": 0.10,
            "question_format": 0.10,
            "power_words": 0.15,
            "clarity": 0.15,
        }
        
        self.thumbnail_factors = {
            "face_present": 0.20,
            "emotion_visible": 0.20,
            "contrast_level": 0.15,
            "text_overlay": 0.15,
            "color_vibrancy": 0.15,
            "simplicity": 0.15,
        }
    
    def predict(
        self,
        title: str,
        thumbnail_description: str = "",
        niche: str = "general",
        audience_type: str = "general"
    ) -> CTRAnalysis:
        """
        Predict CTR based on title and thumbnail elements.
        
        Args:
            title: Video title
            thumbnail_description: Description of thumbnail elements
            niche: Content niche
            audience_type: Target audience type
            
        Returns:
            CTRAnalysis with predicted CTR and breakdown
        """
        logger.info(f"Predicting CTR for title: {title[:50]}...")
        
        # Analyze title
        title_analysis = self._analyze_title(title)
        
        # Analyze thumbnail
        thumbnail_analysis = self._analyze_thumbnail(thumbnail_description)
        
        # Calculate scores
        title_score = sum(title_analysis.values()) / len(title_analysis) * 100
        thumbnail_score = sum(thumbnail_analysis.values()) / len(thumbnail_analysis) * 100
        
        # Weighted final CTR (Title 40%, Thumbnail 60%)
        predicted_ctr = (title_score * 0.4) + (thumbnail_score * 0.6)
        
        # Clamp to realistic range
        predicted_ctr = max(2.0, min(25.0, predicted_ctr))
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            title_analysis, 
            thumbnail_analysis,
            title,
            thumbnail_description
        )
        
        # Compile all factors
        factors = {
            **{f"title_{k}": v for k, v in title_analysis.items()},
            **{f"thumbnail_{k}": v for k, v in thumbnail_analysis.items()},
        }
        
        curiosity_score = title_analysis.get("curiosity_gap", 0.5) * 100
        emotional_impact = title_analysis.get("emotional_words", 0.5) * 100
        clarity_score = title_analysis.get("clarity", 0.5) * 100
        
        return CTRAnalysis(
            predicted_ctr=round(predicted_ctr, 2),
            title_score=round(title_score, 2),
            thumbnail_score=round(thumbnail_score, 2),
            curiosity_score=round(curiosity_score, 2),
            emotional_impact=round(emotional_impact, 2),
            clarity_score=round(clarity_score, 2),
            factors=factors,
            recommendations=recommendations,
            confidence=0.85
        )
    
    def _analyze_title(self, title: str) -> Dict[str, float]:
        """Analyze title for CTR factors."""
        analysis = {
            "length_optimal": 0.5,
            "curiosity_gap": 0.5,
            "emotional_words": 0.5,
            "numbers_present": 0.5,
            "question_format": 0.5,
            "power_words": 0.5,
            "clarity": 0.5,
        }
        
        title_lower = title.lower()
        word_count = len(title.split())
        char_count = len(title)
        
        # Length optimal (40-60 chars is sweet spot)
        if 40 <= char_count <= 60:
            analysis["length_optimal"] = 1.0
        elif 30 <= char_count <= 70:
            analysis["length_optimal"] = 0.7
        elif char_count < 30 or char_count > 70:
            analysis["length_optimal"] = 0.4
        
        # Curiosity gap detection
        curiosity_triggers = [
            "why", "how", "what", "secret", "revealed", "truth",
            "nobody tells", "you need to know", "actually", "really",
            "...", "?", "!", "vs", "versus"
        ]
        if any(trigger in title_lower for trigger in curiosity_triggers):
            analysis["curiosity_gap"] = 0.9
        else:
            analysis["curiosity_gap"] = 0.5
        
        # Emotional words
        emotional_words = [
            "amazing", "shocking", "incredible", "terrible", "beautiful",
            "heartbreaking", "inspiring", "scary", "funny", "awesome",
            "worst", "best", "ultimate", "perfect", "dangerous"
        ]
        emotional_count = sum(1 for word in emotional_words if word in title_lower)
        analysis["emotional_words"] = min(1.0, 0.5 + (emotional_count * 0.25))
        
        # Numbers present
        if any(char.isdigit() for char in title):
            analysis["numbers_present"] = 0.9
        else:
            analysis["numbers_present"] = 0.5
        
        # Question format
        if "?" in title or title_lower.startswith(("how", "why", "what", "when", "where")):
            analysis["question_format"] = 0.85
        else:
            analysis["question_format"] = 0.5
        
        # Power words
        power_words = [
            "proven", "guaranteed", "instant", "free", "new", "exclusive",
            "limited", "breakthrough", "scientific", "expert"
        ]
        power_count = sum(1 for word in power_words if word in title_lower)
        analysis["power_words"] = min(1.0, 0.5 + (power_count * 0.25))
        
        # Clarity (simple language, no jargon overload)
        avg_word_length = sum(len(word) for word in title.split()) / max(1, word_count)
        if avg_word_length < 6:
            analysis["clarity"] = 0.9
        elif avg_word_length < 8:
            analysis["clarity"] = 0.7
        else:
            analysis["clarity"] = 0.5
        
        return analysis
    
    def _analyze_thumbnail(self, description: str) -> Dict[str, float]:
        """Analyze thumbnail description for CTR factors."""
        analysis = {
            "face_present": 0.5,
            "emotion_visible": 0.5,
            "contrast_level": 0.5,
            "text_overlay": 0.5,
            "color_vibrancy": 0.5,
            "simplicity": 0.5,
        }
        
        if not description:
            return analysis
        
        desc_lower = description.lower()
        
        # Face detection keywords
        face_keywords = ["face", "person", "eyes", "expression", "portrait", "headshot"]
        if any(keyword in desc_lower for keyword in face_keywords):
            analysis["face_present"] = 0.95
        
        # Emotion detection
        emotion_keywords = [
            "surprised", "shocked", "happy", "sad", "angry", "excited",
            "smiling", "laughing", "crying", "worried", "amazed"
        ]
        if any(keyword in desc_lower for keyword in emotion_keywords):
            analysis["emotion_visible"] = 0.9
        
        # Contrast indicators
        contrast_keywords = ["bright", "dark", "contrast", "bold", "vivid", "neon"]
        if any(keyword in desc_lower for keyword in contrast_keywords):
            analysis["contrast_level"] = 0.85
        
        # Text overlay
        text_keywords = ["text", "words", "caption", "title", "overlay"]
        if any(keyword in desc_lower for keyword in text_keywords):
            analysis["text_overlay"] = 0.8
        
        # Color vibrancy
        color_keywords = ["colorful", "vibrant", "bright", "red", "blue", "green", "yellow", "orange"]
        if any(keyword in desc_lower for keyword in color_keywords):
            analysis["color_vibrancy"] = 0.85
        
        # Simplicity
        simplicity_keywords = ["simple", "clean", "minimal", "focused", "single"]
        complexity_keywords = ["complex", "busy", "crowded", "multiple", "cluttered"]
        if any(keyword in desc_lower for keyword in simplicity_keywords):
            analysis["simplicity"] = 0.9
        elif any(keyword in desc_lower for keyword in complexity_keywords):
            analysis["simplicity"] = 0.4
        
        return analysis
    
    def _generate_recommendations(
        self,
        title_analysis: Dict[str, float],
        thumbnail_analysis: Dict[str, float],
        title: str,
        thumbnail_desc: str
    ) -> List[str]:
        """Generate actionable recommendations to improve CTR."""
        recommendations = []
        
        # Title recommendations
        if title_analysis.get("length_optimal", 0.5) < 0.7:
            recommendations.append(
                "Optimize title length to 40-60 characters for better visibility"
            )
        
        if title_analysis.get("curiosity_gap", 0.5) < 0.7:
            recommendations.append(
                "Add curiosity triggers like 'secret', 'revealed', or questions"
            )
        
        if title_analysis.get("emotional_words", 0.5) < 0.7:
            recommendations.append(
                "Include emotional words to increase engagement potential"
            )
        
        if title_analysis.get("numbers_present", 0.5) < 0.7:
            recommendations.append(
                "Add numbers to your title (e.g., '5 Ways', '10 Secrets')"
            )
        
        if title_analysis.get("power_words", 0.5) < 0.7:
            recommendations.append(
                "Use power words like 'proven', 'guaranteed', or 'breakthrough'"
            )
        
        # Thumbnail recommendations
        if thumbnail_analysis.get("face_present", 0.5) < 0.7:
            recommendations.append(
                "Consider adding a human face with clear expression to thumbnail"
            )
        
        if thumbnail_analysis.get("emotion_visible", 0.5) < 0.7:
            recommendations.append(
                "Show strong emotions (surprise, excitement) in thumbnail"
            )
        
        if thumbnail_analysis.get("contrast_level", 0.5) < 0.7:
            recommendations.append(
                "Increase contrast and use bold colors for better visibility"
            )
        
        if thumbnail_analysis.get("text_overlay", 0.5) < 0.7 and len(thumbnail_desc) > 0:
            recommendations.append(
                "Add minimal text overlay (3-5 words) to complement the title"
            )
        
        if thumbnail_analysis.get("simplicity", 0.5) < 0.7:
            recommendations.append(
                "Simplify thumbnail design - focus on one main element"
            )
        
        return recommendations[:5]  # Return top 5 recommendations
