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
from research_engine import ResearchEngine, ResearchReport
from channel_intelligence import ChannelAuditor, CompetitorIntelligence
from utils.logger import get_logger, setup_logger

# Setup logging
setup_logger("yt_auto", "INFO", "yt_auto.log")
logger = get_logger(__name__)


# Page configuration
st.set_page_config(
    page_title="YT Auto - Content Intelligence Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


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
        # Research & Intelligence
        st.session_state.research_report = None
        st.session_state.channel_audit = None
        st.session_state.competitor_report = None
        st.session_state.content_calendar = None
        st.session_state.series_plan = None
        st.session_state.title_variations = None
        st.session_state.growth_forecast = None


def render_sidebar():
    """Render sidebar with settings."""
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # AI Provider
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
        st.subheader("📺 Channel Profile")
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
        st.subheader("🔍 Discovery Mode")
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
        
        # Status
        st.subheader("📊 Status")
        st.info(f"Safe Mode: {'✅ On' if safe_mode else '❌ Off'}")
        st.caption(f"AI Provider: {ai_provider}")
        st.caption(f"Discovery: {discovery_mode.replace('_', ' ').title()}")
        
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
    st.header("🔥 Content Opportunities")
    
    # Discovery Mode selection
    discovery_mode = st.session_state.get("discovery_mode", "Dynamic Opportunity Hunter")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_niche = st.text_input(
            "Search by niche (optional)",
            placeholder="e.g., Technology, Health, Business...",
            value="",
        )
    
    with col2:
        limit = st.number_input("Max results", min_value=1, max_value=20, value=10)
    
    if st.button("🔍 Discover Opportunities", type="primary"):
        with st.spinner("Analyzing niche intelligence..."):
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
                st.session_state.last_niche_analysis = result.niche_analysis
                
                # Display summary
                st.success(f"Found {result.total_opportunities} opportunities!")
                
                # Show niche analysis panel if available
                if result.niche_analysis:
                    st.subheader("🎯 Niche Analysis Panel")
                    profile = result.niche_analysis.niche_profile
                    
                    # Niche hierarchy display
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.info(f"**Audience:** {profile.audience}")
                        st.info(f"**Type:** {profile.audience_type.value.title()}")
                    with col_b:
                        st.info(f"**Niche:** {profile.niche.title()}")
                        st.info(f"**Sub-Niche:** {profile.sub_niche}")
                    with col_c:
                        st.info(f"**Topic:** {profile.topic}")
                        st.info(f"**Format:** {profile.format_recommendation.title()}")
                    
                    # Niche Score
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 16px; margin: 16px 0;">
                        <h3 style="color: var(--primary); margin-bottom: 12px;">📊 Niche Score: {profile.niche_score:.1f}/100</h3>
                        <p style="color: var(--text-muted);">{profile.why_selected}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Scoring factors
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        st.progress(profile.audience_size_score, text=f"Audience Size: {profile.audience_size_score:.0%}")
                        st.progress(profile.audience_passion_score, text=f"Audience Passion: {profile.audience_passion_score:.0%}")
                        st.progress(profile.content_depth_score, text=f"Content Depth: {profile.content_depth_score:.0%}")
                    with col_s2:
                        st.progress(profile.repeatability_score, text=f"Repeatability: {profile.repeatability_score:.0%}")
                        st.progress(profile.monetization_potential_score, text=f"Monetization: {profile.monetization_potential_score:.0%}")
                        st.progress(1.0 - profile.competition_score, text=f"Low Competition: {(1.0 - profile.competition_score):.0%}")
                    
                    # SWOT Analysis
                    col_swot1, col_swot2 = st.columns(2)
                    with col_swot1:
                        st.markdown("**✅ Strengths**")
                        for s in profile.strengths:
                            st.caption(f"• {s}")
                        st.markdown("**⚠️ Weaknesses**")
                        for w in profile.weaknesses:
                            st.caption(f"• {w}")
                    with col_swot2:
                        st.markdown("**🚀 Opportunities**")
                        for o in profile.opportunities:
                            st.caption(f"• {o}")
                        st.markdown("**⛔ Threats**")
                        for t in profile.threats:
                            st.caption(f"• {t}")
                    
                    # Additional info
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("Est. Videos Possible", profile.estimated_videos_possible)
                    with col_m2:
                        st.metric("Avg Video Length", profile.avg_video_length)
                    with col_m3:
                        st.metric("Posting Frequency", profile.posting_frequency)
                    
                    # Trending topics from niche analysis
                    if result.trending_niches or result.fastest_growing_topics:
                        st.subheader("📈 Today's Opportunities")
                        if result.trending_niches:
                            st.markdown(f"**Trending Niches:** {', '.join(result.trending_niches)}")
                        if result.fastest_growing_topics:
                            st.markdown("**Fastest Growing Topics:**")
                            for topic in result.fastest_growing_topics[:5]:
                                st.caption(f"• {topic}")
                    
                    # Recommended formats
                    if result.recommended_formats:
                        st.markdown(f"**Recommended Formats:** {', '.join(result.recommended_formats)}")
                
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
    st.header("📊 Analytics Dashboard")
    
    if st.session_state.quality_metrics:
        metrics = st.session_state.quality_metrics
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Originality", f"{metrics.originality_score:.2f}")
        with col2:
            st.metric("Monetization", f"{metrics.monetization_score:.2f}")
        with col3:
            st.metric("Safety", f"{metrics.safety_score:.2f}")
        with col4:
            st.metric("Sources", f"{metrics.source_validation_score:.2f}")
        with col5:
            st.metric("Value Add", f"{metrics.value_add_score:.2f}")
        
        st.divider()
        
        st.metric("Final Content Score", f"{metrics.final_content_score:.2f}")
        
        if metrics.issues:
            st.warning("**Issues Found:**")
            for issue in metrics.issues:
                st.write(f"⚠️ {issue}")
        
        if metrics.recommendations:
            st.success("**Recommendations:**")
            for rec in metrics.recommendations:
                st.write(f"✅ {rec}")
    else:
        st.info("Generate content first to see analytics")


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
    
    # Main title
    st.title("🎬 YT Auto")
    st.caption("YouTube Content Intelligence Platform")
    
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
    st.divider()
    st.caption(
        "YT Auto v1.0 | Built with ❤️ for content creators | "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


if __name__ == "__main__":
    main()
