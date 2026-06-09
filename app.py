"""YT Auto - YouTube Content Intelligence Platform

A professional platform for discovering content opportunities,
generating scripts, SEO optimization, and video planning.
"""

import asyncio
import streamlit as st
from datetime import datetime

# Import configuration
from config.settings import (
    Settings,
    get_settings,
    set_settings,
    AIProvider,
    DiscoveryMode,
    ChannelProfile,
    QualityThresholds,
)
from config.models import (
    ContentFormat,
    Opportunity,
    Topic,
    SEOData,
    Script,
    ThumbnailConcept,
    Storyboard,
    QualityMetrics,
    AnalyticsData,
    ExportPack,
)

# Import engines
from opportunity_engine import OpportunityEngine
from core.engines import SEOEngine, ScriptEngine, ThumbnailEngine, VideoAssembler
from quality_control import QualityEvaluator
from utils.logger import get_logger, setup_logger

# Setup logging
setup_logger("yt_auto", "INFO", "yt_auto.log")
logger = get_logger(__name__)


# ============================================================================
# CUSTOM CSS - PREMIUM DARK FUTURISTIC THEME
# ============================================================================

def inject_custom_css():
    """Inject custom CSS for premium UI/UX."""
    
    st.markdown("""
    <style>
    /* ============================================
       GLOBAL VARIABLES - COLOR PALETTE
       ============================================ */
    :root {
        --bg-primary: #0B1020;
        --bg-surface: #121A2E;
        --bg-card: #16213E;
        --primary: #00D4FF;
        --secondary: #7B61FF;
        --accent: #00FFB2;
        --text-primary: #FFFFFF;
        --text-muted: #A0AEC0;
        --border-color: rgba(0, 212, 255, 0.1);
        --glow-primary: rgba(0, 212, 255, 0.3);
        --glow-secondary: rgba(123, 97, 255, 0.3);
    }

    /* ============================================
       GLOBAL STYLES
       ============================================ */
    .stApp {
        background: linear-gradient(135deg, #0B1020 0%, #0f1623 100%);
        min-height: 100vh;
    }
    
    /* Hide default header */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-surface);
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary), var(--secondary));
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--secondary), var(--primary));
    }

    /* ============================================
       GLASS CARD COMPONENT
       ============================================ */
    .glass-card {
        background: linear-gradient(
            135deg,
            rgba(22, 33, 62, 0.8) 0%,
            rgba(18, 26, 46, 0.9) 100%
        );
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(0, 212, 255, 0.1);
        padding: 24px;
        margin: 16px 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 212, 255, 0.3);
        box-shadow: 
            0 12px 40px rgba(0, 212, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    /* ============================================
       GRADIENT BUTTONS
       ============================================ */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.4);
        background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Secondary button style */
    .secondary-btn > button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
    }

    /* ============================================
       SIDEBAR STYLING
       ============================================ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(11, 16, 32, 0.95) 0%, rgba(18, 26, 46, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 212, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }

    /* Sidebar logo area */
    .sidebar-logo {
        text-align: center;
        padding: 24px 0;
        border-bottom: 1px solid rgba(0, 212, 255, 0.1);
        margin-bottom: 24px;
    }
    
    .sidebar-logo h1 {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .sidebar-logo .version {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 8px;
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: rgba(0, 255, 178, 0.1);
        border: 1px solid rgba(0, 255, 178, 0.3);
        border-radius: 20px;
        font-size: 12px;
        color: var(--accent);
        margin-top: 12px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: var(--accent);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* ============================================
       HEADER / HERO SECTION
       ============================================ */
    .hero-section {
        background: linear-gradient(
            135deg,
            rgba(22, 33, 62, 0.6) 0%,
            rgba(11, 16, 32, 0.8) 100%
        );
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 32px;
        border: 1px solid rgba(0, 212, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 16px 0;
        letter-spacing: -1px;
    }
    
    .hero-tagline {
        font-size: 18px;
        color: var(--text-muted);
        margin: 0 0 8px 0;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .hero-subtitle {
        font-size: 16px;
        color: var(--text-muted);
        margin: 0;
    }
    
    .badge-container {
        display: flex;
        gap: 12px;
        margin-top: 24px;
        flex-wrap: wrap;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        color: var(--primary);
    }
    
    .badge.safe-mode {
        background: rgba(0, 255, 178, 0.1);
        border-color: rgba(0, 255, 178, 0.2);
        color: var(--accent);
    }
    
    .badge.discovery {
        background: rgba(123, 97, 255, 0.1);
        border-color: rgba(123, 97, 255, 0.2);
        color: var(--secondary);
    }

    /* ============================================
       METRIC CARDS
       ============================================ */
    .metric-card {
        background: linear-gradient(
            135deg,
            rgba(22, 33, 62, 0.7) 0%,
            rgba(18, 26, 46, 0.8) 100%
        );
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(0, 212, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 212, 255, 0.3);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.15);
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: var(--text-muted);
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ============================================
       TABS STYLING
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 8px;
        background: rgba(18, 26, 46, 0.5);
        border-radius: 12px;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-muted);
        padding: 12px 24px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1);
        color: var(--primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(123, 97, 255, 0.2));
        color: var(--primary);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }

    /* ============================================
       INPUT FIELDS
       ============================================ */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: rgba(11, 16, 32, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        color: var(--text-primary);
        padding: 12px 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        outline: none;
    }
    
    .stTextInput label,
    .stSelectbox label,
    .stNumberInput label {
        color: var(--text-muted);
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
    }

    /* ============================================
       EXPANDERS
       ============================================ */
    .streamlit-expanderHeader {
        background: rgba(18, 26, 46, 0.5);
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-radius: 12px;
        padding: 16px 20px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(18, 26, 46, 0.8);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    .streamlit-expanderContent {
        background: rgba(11, 16, 32, 0.5);
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-radius: 12px;
        margin-top: 8px;
        padding: 20px;
    }

    /* ============================================
       CODE BLOCKS
       ============================================ */
    pre.stCodeBlock {
        background: rgba(11, 16, 32, 0.9);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
    }
    
    code {
        color: var(--accent) !important;
    }

    /* ============================================
       PROGRESS BAR
       ============================================ */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 10px;
    }
    
    .stProgress > div > div {
        background: rgba(18, 26, 46, 0.8);
        border-radius: 10px;
        border: 1px solid rgba(0, 212, 255, 0.1);
    }

    /* ============================================
       ALERTS & MESSAGES
       ============================================ */
    .stAlert {
        border-radius: 12px;
        border: none;
    }
    
    .stSuccess {
        background: rgba(0, 255, 178, 0.1);
        border: 1px solid rgba(0, 255, 178, 0.3);
    }
    
    .stError {
        background: rgba(255, 82, 82, 0.1);
        border: 1px solid rgba(255, 82, 82, 0.3);
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid rgba(255, 193, 7, 0.3);
    }
    
    .stInfo {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }

    /* ============================================
       DIVIDER
       ============================================ */
    hr {
        border-color: rgba(0, 212, 255, 0.1) !important;
    }

    /* ============================================
       LOADING ANIMATION
       ============================================ */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading-shimmer {
        background: linear-gradient(
            90deg,
            rgba(0, 212, 255, 0.1) 0%,
            rgba(0, 212, 255, 0.2) 50%,
            rgba(0, 212, 255, 0.1) 100%
        );
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
        border-radius: 12px;
        padding: 20px;
    }

    /* ============================================
       FOOTER
       ============================================ */
    .footer {
        text-align: center;
        padding: 32px 0;
        margin-top: 48px;
        border-top: 1px solid rgba(0, 212, 255, 0.1);
        color: var(--text-muted);
        font-size: 14px;
    }
    
    .footer-heart {
        color: #ff6b6b;
    }

    /* ============================================
       RESPONSIVE ADJUSTMENTS
       ============================================ */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px;
        }
        
        .hero-tagline {
            font-size: 14px;
        }
        
        .metric-value {
            font-size: 28px;
        }
        
        .badge-container {
            justify-content: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# Page configuration
st.set_page_config(
    page_title="YT Auto - Content Intelligence Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
inject_custom_css()


def init_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.safe_mode = True
        st.session_state.ai_provider = "mock"
        st.session_state.discovery_mode = "dynamic_opportunity"
        st.session_state.channel_niche = "General"
        st.session_state.current_opportunities = []
        st.session_state.current_topic = None
        st.session_state.generated_seo = None
        st.session_state.generated_script = None
        st.session_state.generated_thumbnail = None
        st.session_state.generated_storyboard = None
        st.session_state.quality_metrics = None
        st.session_state.analytics = None


def render_sidebar():
    """Render sidebar with settings."""
    with st.sidebar:
        # Logo area
        st.markdown("""
        <div class="sidebar-logo">
            <h1>🎬 YT Auto</h1>
            <div class="version">v1.0.0</div>
            <div class="status-indicator">
                <span class="status-dot"></span>
                System Online
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Provider
        st.markdown("### 🔧 AI Configuration")
        ai_provider = st.selectbox(
            "AI Provider",
            options=["mock", "openai", "anthropic", "google", "ollama"],
            index=0,
            help="Select AI provider for content generation",
        )
        st.session_state.ai_provider = ai_provider
        
        # Safe Mode
        safe_mode = st.toggle(
            "Safe Mode",
            value=st.session_state.safe_mode,
            help="Enable content safety checks",
        )
        st.session_state.safe_mode = safe_mode
        
        st.divider()
        
        # Channel Profile
        st.markdown("### 📺 Channel Profile")
        channel_name = st.text_input("Channel Name", value="My Channel")
        channel_niche = st.selectbox(
            "Niche",
            options=[
                "General",
                "Technology",
                "Health",
                "Business",
                "Education",
                "Entertainment",
                "Lifestyle",
                "Science",
            ],
            index=0,
        )
        st.session_state.channel_niche = channel_niche
        
        target_audience = st.text_input("Target Audience", value="General audience")
        content_style = st.selectbox(
            "Content Style",
            options=["Educational", "Entertaining", "Professional", "Casual"],
            index=0,
        )
        
        st.divider()
        
        # Discovery Mode
        st.markdown("### 🔍 Discovery Mode")
        discovery_mode = st.radio(
            "Mode",
            options=["fixed_niche", "dynamic_opportunity"],
            format_func=lambda x: "Fixed Niche" if x == "fixed_niche" else "Dynamic Hunter",
            index=1,
        )
        st.session_state.discovery_mode = discovery_mode
        
        if discovery_mode == "fixed_niche":
            fixed_niche = st.text_input("Fixed Niche", value=channel_niche)
        
        st.divider()
        
        # Status badges
        st.markdown("### 📊 Status")
        col1, col2 = st.columns(2)
        with col1:
            if safe_mode:
                st.markdown("""
                <div class="badge safe-mode" style="display:inline-flex;">
                    ✅ Safe Mode
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="badge" style="display:inline-flex;">
                    ⚠️ Standard
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="badge discovery" style="display:inline-flex;font-size:11px;">
                {discovery_mode.replace('_', ' ').title()}
            </div>
            """, unsafe_allow_html=True)
        
        st.caption(f"AI: {ai_provider}")
        
        return {
            "ai_provider": ai_provider,
            "safe_mode": safe_mode,
            "channel_name": channel_name,
            "channel_niche": channel_niche,
            "target_audience": target_audience,
            "content_style": content_style,
            "discovery_mode": discovery_mode,
        }


def render_opportunities_tab(opportunity_engine: OpportunityEngine):
    """Render Opportunities tab."""
    # Metric cards at top
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 20px;">🔥 Content Opportunities</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <p class="metric-value">0</p>
            <p class="metric-label">Trending Topics</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <p class="metric-value">0</p>
            <p class="metric-label">High Opportunity Niches</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <p class="metric-value">--</p>
            <p class="metric-label">Avg Opportunity Score</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <p class="metric-value">{count}</p>
            <p class="metric-label">Ideas Generated</p>
        </div>
        """.format(count=len(st.session_state.current_opportunities)), unsafe_allow_html=True)
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_niche = st.text_input(
            "Search by niche (optional)",
            placeholder="e.g., AI, Health, Business...",
        )
    
    with col2:
        limit = st.number_input("Max results", min_value=1, max_value=20, value=10)
    
    if st.button("🔍 Discover Opportunities", type="primary"):
        with st.spinner("Scanning for opportunities..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if search_niche:
                    result = loop.run_until_complete(
                        opportunity_engine.discover_fixed_niche(search_niche, limit)
                    )
                else:
                    result = loop.run_until_complete(
                        opportunity_engine.discover_dynamic(limit)
                    )
                
                st.session_state.current_opportunities = result.ranked_topics
                
                # Display summary
                st.success(f"Found {result.total_opportunities} opportunities!")
                
                # Show recommendations
                if result.recommendations:
                    st.subheader("💡 Recommendations")
                    for rec in result.recommendations:
                        st.markdown(f"- {rec}")
                
            except Exception as e:
                st.error(f"Error discovering opportunities: {str(e)}")
                logger.error(f"Opportunity discovery error: {e}")
    
    # Display opportunities
    if st.session_state.current_opportunities:
        st.subheader(f"📋 Top Opportunities ({len(st.session_state.current_opportunities)})")
        
        for i, topic in enumerate(st.session_state.current_opportunities):
            with st.expander(f"#{i+1}: {topic.title} (Score: {topic.opportunity_score:.2f})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Trend Score", f"{topic.trend_score:.2f}")
                    st.metric("Demand Score", f"{topic.demand_score:.2f}")
                with col2:
                    st.metric("Gap Score", f"{topic.gap_score:.2f}")
                    st.metric("Feasibility", f"{topic.feasibility_score:.2f}")
                with col3:
                    st.metric("Potential Reach", f"{topic.potential_reach:,}")
                    st.caption(f"Effort: {topic.estimated_effort}")
                
                st.write(f"**Description:** {topic.description}")
                st.write(f"**Niche:** {topic.niche}")
                st.write(f"**Recommended Format:** {topic.format_recommendation}")
                
                if topic.keywords:
                    st.write(f"**Keywords:** {', '.join(topic.keywords)}")
                
                if st.button(f"Select This Topic", key=f"select_{i}"):
                    st.session_state.current_topic = topic
                    st.success(f"Selected: {topic.title}")


def render_topics_tab():
    """Render Topics tab."""
    st.header("🎯 Selected Topic")
    
    if st.session_state.current_topic:
        topic = st.session_state.current_topic
        
        st.subheader(topic.title)
        st.write(topic.description)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Opportunity Score", f"{topic.opportunity_score:.2f}")
        with col2:
            st.metric("Niche", topic.niche)
        with col3:
            st.metric("Format", topic.format_recommendation)
        
        st.divider()
        
        st.write("**Keywords:**")
        st.write(", ".join(topic.keywords) if topic.keywords else "None")
    else:
        st.info("👈 Select a topic from the Opportunities tab first")


def render_formats_tab():
    """Render Formats tab."""
    st.header("🎬 Content Formats")
    
    formats = {
        "Documentary": "Long-form deep dives into subjects",
        "Explainer": "Clear, educational breakdowns",
        "Storytelling": "Narrative-driven content",
        "News": "Current events and updates",
        "Shorts": "Quick, vertical videos under 60s",
        "Animation": "Animated content with motion graphics",
        "Motion Graphics": "Visual-heavy explanatory content",
        "Hybrid": "Mixed format approaches",
        "Crime Documentary": "True crime investigations",
        "History Documentary": "Historical deep dives",
    }
    
    cols = st.columns(2)
    for i, (fmt, desc) in enumerate(formats.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(fmt)
                st.write(desc)
    
    if st.session_state.current_topic:
        st.divider()
        st.success(f"Recommended for your topic: **{st.session_state.current_topic.format_recommendation}**")


def render_templates_tab():
    """Render Templates tab."""
    st.header("🎨 Content Templates")
    
    templates = {
        "Hook Templates": [
            "What if everything you knew about X was wrong?",
            "The truth about X nobody tells you",
            "I tried X for 30 days, here's what happened",
            "X explained in under 10 minutes",
        ],
        "Intro Templates": [
            "Welcome back! Today we're diving into...",
            "Have you ever wondered about...?",
            "In this video, we'll explore...",
        ],
        "CTA Templates": [
            "If you found this helpful, smash that like button!",
            "Subscribe for more content like this!",
            "Let me know your thoughts in the comments!",
        ],
    }
    
    for template_type, templates_list in templates.items():
        with st.expander(template_type):
            for template in templates_list:
                st.write(f"• {template}")


def render_seo_tab(seo_engine: SEOEngine):
    """Render SEO tab."""
    st.header("📈 SEO Optimization")
    
    if not st.session_state.current_topic:
        st.info("👈 Select a topic from the Opportunities tab first")
        return
    
    topic = st.session_state.current_topic
    
    if st.button("🚀 Generate SEO Pack", type="primary"):
        with st.spinner("Generating SEO data..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                seo_data = loop.run_until_complete(
                    seo_engine.generate(
                        topic=topic.title,
                        description=topic.description,
                        niche=topic.niche,
                        target_keywords=topic.keywords,
                    )
                )
                
                st.session_state.generated_seo = seo_data
                
                st.success("SEO pack generated!")
                
            except Exception as e:
                st.error(f"Error generating SEO: {str(e)}")
    
    if st.session_state.generated_seo:
        seo = st.session_state.generated_seo
        
        st.subheader("Generated SEO Data")
        
        st.write("**Title:**")
        st.code(seo.title)
        
        st.write("**Description:**")
        st.text_area("Description", seo.description, height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Tags:**")
            st.write(", ".join(seo.tags))
        
        with col2:
            st.write("**Keywords:**")
            st.write(", ".join(seo.keywords))
        
        st.write(f"**Category:** {seo.category}")


def render_script_tab(script_engine: ScriptEngine):
    """Render Script tab."""
    st.header("✍️ Script Generation")
    
    if not st.session_state.current_topic:
        st.info("👈 Select a topic from the Opportunities tab first")
        return
    
    topic = st.session_state.current_topic
    
    col1, col2 = st.columns(2)
    with col1:
        duration = st.slider("Target Duration (minutes)", 1, 30, 10)
    with col2:
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Enthusiastic", "Dramatic", "Educational"],
        )
    
    if st.button("📝 Generate Script", type="primary"):
        with st.spinner("Writing script..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                format_map = {
                    "documentary": ContentFormat.DOCUMENTARY,
                    "explainer": ContentFormat.EXPLAINER,
                    "storytelling": ContentFormat.STORYTELLING,
                    "news": ContentFormat.NEWS,
                    "shorts": ContentFormat.SHORTS,
                    "animation": ContentFormat.ANIMATION,
                }
                fmt = format_map.get(topic.format_recommendation, ContentFormat.EXPLAINER)
                
                script = loop.run_until_complete(
                    script_engine.generate(
                        topic=topic.title,
                        description=topic.description,
                        format_type=fmt,
                        target_duration_seconds=duration * 60,
                        tone=tone.lower(),
                    )
                )
                
                st.session_state.generated_script = script
                st.success("Script generated!")
                
            except Exception as e:
                st.error(f"Error generating script: {str(e)}")
    
    if st.session_state.generated_script:
        script = st.session_state.generated_script
        
        st.subheader(f"Script: {script.title}")
        
        st.write(f"**Total Duration:** {script.total_duration_seconds // 60} minutes")
        st.write(f"**Word Count:** {script.word_count} words")
        st.write(f"**Format:** {script.format.value}")
        
        for section in script.sections:
            with st.expander(f"{section.section_type.upper()} ({section.duration_seconds}s)"):
                st.write(section.content)
                if section.visual_cues:
                    st.write("**Visual Cues:**")
                    for cue in section.visual_cues:
                        st.write(f"• {cue}")


def render_thumbnail_tab(thumbnail_engine: ThumbnailEngine):
    """Render Thumbnail tab."""
    st.header("🖼️ Thumbnail Generator")
    
    if not st.session_state.current_topic:
        st.info("👈 Select a topic from the Opportunities tab first")
        return
    
    topic = st.session_state.current_topic
    
    if st.button("🎨 Generate Thumbnail Concept", type="primary"):
        with st.spinner("Designing thumbnail..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                format_map = {
                    "documentary": ContentFormat.DOCUMENTARY,
                    "explainer": ContentFormat.EXPLAINER,
                    "storytelling": ContentFormat.STORYTELLING,
                    "news": ContentFormat.NEWS,
                    "shorts": ContentFormat.SHORTS,
                    "animation": ContentFormat.ANIMATION,
                }
                fmt = format_map.get(topic.format_recommendation, ContentFormat.EXPLAINER)
                
                concept = loop.run_until_complete(
                    thumbnail_engine.generate(
                        topic=topic.title,
                        format_type=fmt,
                    )
                )
                
                st.session_state.generated_thumbnail = concept
                st.success("Thumbnail concept generated!")
                
            except Exception as e:
                st.error(f"Error generating thumbnail: {str(e)}")
    
    if st.session_state.generated_thumbnail:
        concept = st.session_state.generated_thumbnail
        
        st.subheader("Thumbnail Concept")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Main Text:**")
            st.write(concept.main_text)
            
            st.write("**Secondary Text:**")
            st.write(concept.secondary_text or "None")
            
            st.write("**Color Scheme:**")
            st.write(concept.color_scheme)
        
        with col2:
            st.metric("Estimated CTR", f"{concept.ctr_score:.2f}")
            
            st.write("**Mood:**")
            st.write(concept.mood)
        
        st.write("**Elements:**")
        for element in concept.elements:
            st.write(f"• {element}")
        
        st.divider()
        st.write("**AI Image Prompt:**")
        st.code(concept.prompt)


def render_research_tab():
    """Render Research tab."""
    st.header("📚 Research & Sources")
    
    st.info("Research features coming soon. This will include:")
    
    features = [
        "Source validation and tracking",
        "Fact-checking assistance",
        "Reference management",
        "Competitor analysis",
        "Trend research archive",
    ]
    
    for feature in features:
        st.write(f"• {feature}")


def render_analytics_tab():
    """Render Analytics tab."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 20px;">📊 Analytics Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.quality_metrics:
        metrics = st.session_state.quality_metrics
        
        # KPI Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{value}</p>
                <p class="metric-label">Originality</p>
            </div>
            """.format(value=f"{metrics.originality_score:.2f}"), unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{value}</p>
                <p class="metric-label">Monetization</p>
            </div>
            """.format(value=f"{metrics.monetization_score:.2f}"), unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{value}</p>
                <p class="metric-label">Safety</p>
            </div>
            """.format(value=f"{metrics.safety_score:.2f}"), unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{value}</p>
                <p class="metric-label">Sources</p>
            </div>
            """.format(value=f"{metrics.source_validation_score:.2f}"), unsafe_allow_html=True)
        with col5:
            st.markdown("""
            <div class="metric-card">
                <p class="metric-value">{value}</p>
                <p class="metric-label">Value Add</p>
            </div>
            """.format(value=f"{metrics.value_add_score:.2f}"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
        
        # Final score in a larger card
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 32px;">
            <p style="font-size: 18px; color: var(--text-muted); margin-bottom: 16px;">FINAL CONTENT SCORE</p>
            <p class="metric-value" style="font-size: 56px;">{score}</p>
        </div>
        """.format(score=f"{metrics.final_content_score:.2f}"), unsafe_allow_html=True)
        
        if metrics.issues:
            st.markdown("### ⚠️ Issues Found")
            for issue in metrics.issues:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #ffc107; padding: 16px 20px;">
                    ⚠️ {issue}
                </div>
                """, unsafe_allow_html=True)
        
        if metrics.recommendations:
            st.markdown("### ✅ Recommendations")
            for rec in metrics.recommendations:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #00ffb2; padding: 16px 20px;">
                    ✅ {rec}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 48px;">
            <p style="font-size: 18px; color: var(--text-muted);">Generate content first to see analytics</p>
        </div>
        """, unsafe_allow_html=True)


def render_settings_tab(settings: dict):
    """Render Settings tab."""
    st.header("⚙️ Application Settings")
    
    st.subheader("Current Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**AI Provider:**", settings.get("ai_provider", "mock"))
        st.write("**Safe Mode:**", "Enabled" if settings.get("safe_mode") else "Disabled")
        st.write("**Discovery Mode:**", settings.get("discovery_mode", "dynamic"))
    
    with col2:
        st.write("**Channel:**", settings.get("channel_name", "My Channel"))
        st.write("**Niche:**", settings.get("channel_niche", "General"))
        st.write("**Style:**", settings.get("content_style", "Educational"))
    
    st.divider()
    
    st.subheader("Export Settings")
    
    export_format = st.selectbox(
        "Export Format",
        ["JSON", "Markdown", "TXT"],
    )
    
    st.info("Export functionality coming soon")


def run_quality_check(script: Script, topic) -> QualityMetrics:
    """Run quality check on generated content."""
    evaluator = QualityEvaluator()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    metrics = loop.run_until_complete(
        evaluator.evaluate(
            script=script,
            topic=topic.title if hasattr(topic, 'title') else str(topic),
            niche=topic.niche if hasattr(topic, 'niche') else "general",
        )
    )
    
    return metrics


def main():
    """Main application entry point."""
    init_session_state()
    
    # Render sidebar and get settings
    settings = render_sidebar()
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎬 YT Auto</h1>
        <p class="hero-tagline">Discover. Analyze. Create. Grow.</p>
        <p class="hero-subtitle">YouTube Content Intelligence Platform</p>
        <div class="badge-container">
            <div class="badge safe-mode">
                ✅ Safe Mode: {safe_mode}
            </div>
            <div class="badge">
                🤖 AI: {ai_provider}
            </div>
            <div class="badge discovery">
                🔍 {discovery_mode}
            </div>
        </div>
    </div>
    """.format(
        safe_mode="On" if settings["safe_mode"] else "Off",
        ai_provider=settings["ai_provider"].upper(),
        discovery_mode=settings["discovery_mode"].replace("_", " ").title()
    ), unsafe_allow_html=True)
    
    # Create tabs
    tabs = st.tabs([
        "🔥 Opportunities",
        "🎯 Topics",
        "🎬 Formats",
        "🎨 Templates",
        "📈 SEO",
        "✍️ Script",
        "🖼️ Thumbnail",
        "📚 Research",
        "📊 Analytics",
        "⚙️ Settings",
    ])
    
    # Initialize engines
    opportunity_engine = OpportunityEngine()
    seo_engine = SEOEngine()
    script_engine = ScriptEngine()
    thumbnail_engine = ThumbnailEngine()
    
    # Render each tab
    with tabs[0]:
        render_opportunities_tab(opportunity_engine)
    
    with tabs[1]:
        render_topics_tab()
    
    with tabs[2]:
        render_formats_tab()
    
    with tabs[3]:
        render_templates_tab()
    
    with tabs[4]:
        render_seo_tab(seo_engine)
    
    with tabs[5]:
        render_script_tab(script_engine)
    
    with tabs[6]:
        render_thumbnail_tab(thumbnail_engine)
    
    with tabs[7]:
        render_research_tab()
    
    with tabs[8]:
        # Run quality check if script is generated
        if st.session_state.generated_script and st.session_state.current_topic:
            if st.session_state.quality_metrics is None:
                with st.spinner("Running quality check..."):
                    metrics = run_quality_check(
                        st.session_state.generated_script,
                        st.session_state.current_topic,
                    )
                    st.session_state.quality_metrics = metrics
        
        render_analytics_tab()
    
    with tabs[9]:
        render_settings_tab(settings)
    
    # Footer
    st.markdown("""
    <div class="footer">
        YT Auto v1.0 | Built with <span class="footer-heart">❤️</span> for content creators | 
        Last updated: {datetime}
    </div>
    """.format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
