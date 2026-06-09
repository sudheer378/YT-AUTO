"""YT Auto Configuration Settings."""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import os


class AIProvider(str, Enum):
    """AI Provider enumeration."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    MOCK = "mock"


class DiscoveryMode(str, Enum):
    """Discovery mode enumeration."""
    FIXED_NICHE = "fixed_niche"
    DYNAMIC_OPPORTUNITY = "dynamic_opportunity"


@dataclass
class ChannelProfile:
    """Channel profile configuration."""
    name: str = "Default Channel"
    niche: str = "General"
    target_audience: str = "General audience"
    content_style: str = "Educational"
    video_length: str = "10-15 minutes"
    upload_frequency: str = "Weekly"
    tone: str = "Professional yet approachable"


@dataclass
class QualityThresholds:
    """Quality control thresholds."""
    min_originality_score: float = 0.7
    min_monetization_score: float = 0.6
    min_safety_score: float = 0.8
    min_source_validation: float = 0.7
    min_value_add: float = 0.6
    min_final_content_score: float = 0.7


@dataclass
class Settings:
    """Application settings."""
    # AI Configuration
    ai_provider: AIProvider = AIProvider.MOCK
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    
    # Safety
    safe_mode: bool = True
    
    # Discovery
    discovery_mode: DiscoveryMode = DiscoveryMode.DYNAMIC_OPPORTUNITY
    
    # Channel
    channel_profile: ChannelProfile = field(default_factory=ChannelProfile)
    
    # Quality
    quality_thresholds: QualityThresholds = field(default_factory=QualityThresholds)
    
    # Paths
    workspace_dir: str = "workspace"
    output_dir: str = "output"
    assets_dir: str = "assets"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "yt_auto.log"
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        return cls(
            ai_provider=AIProvider(os.getenv("AI_PROVIDER", "mock")),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            safe_mode=os.getenv("SAFE_MODE", "true").lower() == "true",
            discovery_mode=DiscoveryMode(os.getenv("DISCOVERY_MODE", "dynamic_opportunity")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
    
    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return {
            "ai_provider": self.ai_provider.value,
            "safe_mode": self.safe_mode,
            "discovery_mode": self.discovery_mode.value,
            "channel_profile": {
                "name": self.channel_profile.name,
                "niche": self.channel_profile.niche,
                "target_audience": self.channel_profile.target_audience,
                "content_style": self.channel_profile.content_style,
                "video_length": self.channel_profile.video_length,
                "upload_frequency": self.channel_profile.upload_frequency,
                "tone": self.channel_profile.tone,
            },
            "quality_thresholds": {
                "min_originality_score": self.quality_thresholds.min_originality_score,
                "min_monetization_score": self.quality_thresholds.min_monetization_score,
                "min_safety_score": self.quality_thresholds.min_safety_score,
                "min_source_validation": self.quality_thresholds.min_source_validation,
                "min_value_add": self.quality_thresholds.min_value_add,
                "min_final_content_score": self.quality_thresholds.min_final_content_score,
            },
        }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def set_settings(settings: Settings) -> None:
    """Set global settings instance."""
    global _settings
    _settings = settings
