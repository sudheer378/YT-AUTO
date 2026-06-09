"""YT Auto Configuration Models."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ContentFormat(str, Enum):
    """Content format enumeration."""
    DOCUMENTARY = "documentary"
    ANIMATION = "animation"
    MOTION_GRAPHICS = "motion_graphics"
    EXPLAINER = "explainer"
    STORYTELLING = "storytelling"
    NEWS = "news"
    SHORTS = "shorts"
    HYBRID = "hybrid"
    CRIME_DOCUMENTARY = "crime_documentary"
    HISTORY_DOCUMENTARY = "history_documentary"


@dataclass
class Opportunity:
    """Represents a content opportunity."""
    topic: str
    niche: str
    trend_score: float
    demand_score: float
    competition_score: float
    opportunity_score: float
    description: str
    keywords: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class Topic:
    """Represents a video topic."""
    title: str
    description: str
    niche: str
    format: ContentFormat
    target_audience: str
    estimated_duration: str
    difficulty: str
    potential_views: int
    keywords: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)


@dataclass
class SEOData:
    """SEO data for a video."""
    title: str
    description: str
    tags: List[str]
    keywords: List[str]
    category: str
    language: str = "en"


@dataclass
class ScriptSection:
    """A section of a video script."""
    section_type: str  # hook, intro, body, cta
    content: str
    duration_seconds: int = 60
    visual_cues: List[str] = field(default_factory=list)


@dataclass
class Script:
    """Complete video script."""
    title: str
    topic: str
    format: ContentFormat
    sections: List[ScriptSection]
    total_duration_seconds: int
    word_count: int
    notes: str = ""


@dataclass
class ThumbnailConcept:
    """Thumbnail concept data."""
    concept_description: str
    main_text: str
    secondary_text: str = ""
    color_scheme: str = ""
    mood: str = ""
    elements: List[str] = field(default_factory=list)
    ctr_score: float = 0.5
    prompt: str = ""


@dataclass
class StoryboardScene:
    """A scene in the storyboard."""
    scene_number: int
    description: str
    duration_seconds: int
    visual_prompt: str
    audio_prompt: str = ""
    transition: str = "cut"
    assets_needed: List[str] = field(default_factory=list)


@dataclass
class Storyboard:
    """Complete storyboard for a video."""
    title: str
    scenes: List[StoryboardScene]
    total_duration_seconds: int
    style_notes: str = ""


@dataclass
class QualityMetrics:
    """Quality control metrics."""
    originality_score: float
    monetization_score: float
    safety_score: float
    source_validation_score: float
    value_add_score: float
    final_content_score: float
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class AnalyticsData:
    """Analytics tracking data."""
    opportunity_score: float
    seo_score: float
    safety_score: float
    ctr_score: float
    retention_prediction: float
    overall_score: float
    timestamp: str = ""


@dataclass
class ExportPack:
    """Export pack containing all generated content."""
    seo_pack: SEOData
    script: Script
    thumbnail_concept: ThumbnailConcept
    storyboard: Storyboard
    quality_metrics: QualityMetrics
    analytics: AnalyticsData
    metadata: dict = field(default_factory=dict)
