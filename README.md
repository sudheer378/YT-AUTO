# YT Auto - YouTube Content Intelligence Platform

A professional platform for discovering content opportunities, generating scripts, SEO optimization, and video planning.

## Features

### 🔥 Opportunity Discovery
- **Trend Scanner**: Scans internet trends and platforms for emerging topics
- **Demand Validator**: Validates audience demand using multiple signals
- **Niche Gap Finder**: Identifies underserved niches and content gaps
- **Topic Ranker**: Ranks opportunities by potential impact

### 🎯 Core Engines
- **SEO Engine**: Generates optimized titles, descriptions, tags, and keywords
- **Script Engine**: Creates complete video scripts with hooks, intros, body, and CTAs
- **Thumbnail Engine**: Designs thumbnail concepts with AI image prompts
- **Video Assembler**: Creates storyboards and production plans

### 📊 Quality Control
- Originality Score
- Monetization Score
- Safety Score
- Source Validation
- Value Add Validation

### 🎬 Format Support
- Documentary
- Animation
- Motion Graphics
- Explainer
- Storytelling
- News
- Shorts
- Hybrid
- Crime Documentary
- History Documentary

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run the Dashboard
```bash
python -m streamlit run app.py
```

Or use the run script:
```bash
python run.py
```

### Direct Python Import
```python
from opportunity_engine import OpportunityEngine
from core.engines import SEOEngine, ScriptEngine, ThumbnailEngine

# Discover opportunities
engine = OpportunityEngine()
result = await engine.discover(niche="technology", limit=10)

# Generate SEO data
seo_engine = SEOEngine()
seo = await seo_engine.generate(topic="AI Explained", description="...", niche="technology")

# Generate script
script_engine = ScriptEngine()
script = await script_engine.generate(topic="AI Explained", format_type=ContentFormat.EXPLAINER)
```

## Architecture

```
YT-Auto/
├── app.py                 # Streamlit dashboard
├── run.py                 # Run script
├── requirements.txt       # Dependencies
├── config/                # Configuration and models
│   ├── settings.py        # App settings
│   └── models.py          # Data models
├── core/                  # Core functionality
│   ├── ai_client.py       # AI provider integration
│   ├── base_engine.py     # Base engine class
│   └── engines/           # Content engines
│       ├── seo_engine.py
│       ├── script_engine.py
│       ├── thumbnail_engine.py
│       └── video_assembler.py
├── opportunity_engine/    # Opportunity discovery
│   ├── trend_scanner.py
│   ├── demand_validator.py
│   ├── niche_gap_finder.py
│   ├── topic_ranker.py
│   └── engine.py
├── quality_control/       # Quality evaluation
│   └── evaluator.py
├── utils/                 # Utilities
│   ├── logger.py
│   └── helpers.py
└── workspace/             # Working directory
└── output/                # Generated content
```

## Configuration

Set environment variables or use the dashboard settings:

```bash
export AI_PROVIDER=mock  # mock, openai, anthropic, google, ollama
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
export GOOGLE_API_KEY=your_key
export SAFE_MODE=true
```

## Dashboard Tabs

1. **🔥 Opportunities**: Discover trending content opportunities
2. **🎯 Topics**: View selected topic details
3. **🎬 Formats**: Explore content format options
4. **🎨 Templates**: Access hook, intro, and CTA templates
5. **📈 SEO**: Generate SEO-optimized metadata
6. **✍️ Script**: Create complete video scripts
7. **🖼️ Thumbnail**: Design thumbnail concepts
8. **📚 Research**: (Coming soon) Source validation and fact-checking
9. **📊 Analytics**: View quality metrics and scores
10. **⚙️ Settings**: Configure application settings

## Workflow

```
Internet Trends
    ↓
Opportunity Discovery
    ↓
Topic Discovery
    ↓
Format Discovery
    ↓
Template Discovery
    ↓
Research
    ↓
SEO
    ↓
Script
    ↓
Thumbnail
    ↓
Storyboard
    ↓
Safety Check
    ↓
Analytics
    ↓
Export Pack
```

## AI Providers

The platform supports multiple AI providers:

- **Mock**: Default, no API key required (for testing)
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3 models
- **Google**: Gemini Pro
- **Ollama**: Local LLM support

## Safety Features

- Safe Mode enabled by default
- Content safety scoring
- Monetization compliance checks
- Source validation
- Policy compliance screening

## License

MIT License

## Version

1.0.0