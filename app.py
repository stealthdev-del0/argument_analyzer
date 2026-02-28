"""
Argument Structure Analyzer - Streamlit Web App
GUI für interaktive Argument-Analyse
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from preprocessing import TextPreprocessor
from claim_detection import ClaimDetector
from emotion_analysis import EmotionAnalyzer
from argument_classification import ArgumentClassifier
from structure_builder import StructureBuilder
from test_cases import list_test_cases, get_test_case

# Page config
st.set_page_config(
    page_title="🧠 Argument Structure Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .argument-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Input method
    input_method = st.radio(
        "Select Input Method:",
        ["📝 Free Text", "📂 Example Cases"],
        help="Choose how to input text for analysis"
    )
    
    # Min confidence threshold
    min_confidence = st.slider(
        "Minimum Confidence Threshold:",
        0.0, 1.0, 0.6,
        help="Filter arguments by minimum confidence"
    )
    
    st.divider()
    st.markdown("### 📊 About")
    st.markdown("""
    **Argument Structure Analyzer** analyzes text for:
    - 🟢 Main claims
    - 🔵 Supporting arguments
    - 🟣 Counter arguments
    - 😊 Sentiment & emotionality
    - 🔴 Logical weaknesses
    """)

# Main content
st.title("🧠 Argument Structure Analyzer")
st.markdown("*Analyze argumentative structures in any text*")

st.divider()

# Input section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Input Text")
    
    if input_method == "📝 Free Text":
        text_input = st.text_area(
            "Enter or paste your text:",
            value=st.session_state.text_input,
            height=200,
            placeholder="Enter your text here... (essay, comment, debate, etc.)",
            label_visibility="collapsed"
        )
    else:
        selected_case = st.selectbox(
            "Select Example Case:",
            list_test_cases(),
            format_func=lambda x: x.replace("_", " ").title()
        )
        text_input = get_test_case(selected_case)
        st.info(f"ℹ️ Loaded example: **{selected_case.replace('_', ' ').title()}**")

with col2:
    st.subheader("📊 Stats")
    if text_input:
        words = len(text_input.split())
        chars = len(text_input)
        st.metric("Characters", f"{chars:,}")
        st.metric("Words", f"{words:,}")
        st.metric("Est. Sentences", f"~{max(1, chars // 50)}")

st.divider()

# Analysis button
if st.button("🚀 Analyze", use_container_width=True, type="primary"):
    if text_input.strip():
        with st.spinner("⏳ Analyzing text..."):
            try:
                # Initialize components
                processor = TextPreprocessor()
                classifier = ArgumentClassifier()
                builder = StructureBuilder()
                
                # Process
                sentences = processor.process_text(text_input)
                classifications = classifier.classify_arguments(sentences)
                root_claims = builder.build_structure(classifications)
                
                # Store results
                st.session_state.analysis_results = {
                    'sentences': sentences,
                    'classifications': classifications,
                    'builder': builder,
                    'argument_summary': classifier.get_argument_summary(classifications),
                    'emotion_summary': EmotionAnalyzer().get_sentiment_summary(
                        EmotionAnalyzer().analyze_emotions(sentences)
                    )
                }
                
                st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
    else:
        st.warning("⚠️ Please enter some text to analyze")

# Results section
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    st.divider()
    st.header("📊 Analysis Results")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        claim_count = results['argument_summary']['CLAIM']['count']
        st.metric("🟢 Claims", claim_count)
    
    with col2:
        support_count = results['argument_summary']['SUPPORT']['count']
        st.metric("🔵 Supports", support_count)
    
    with col3:
        counter_count = results['argument_summary']['COUNTER']['count']
        st.metric("🟣 Counters", counter_count)
    
    with col4:
        avg_strength = results['argument_summary']['CLAIM']['avg_strength'] if claim_count > 0 else 0
        st.metric("💪 Avg Strength", f"{avg_strength:.1%}")
    
    st.divider()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Arguments", "🌳 Structure", "😊 Emotions", "🔴 Weaknesses", "📈 Details"]
    )
    
    # Tab 1: Arguments
    with tab1:
        st.subheader("Classified Arguments")
        
        # Filter by type
        arg_filter = st.multiselect(
            "Filter by type:",
            ["CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"],
            default=["CLAIM", "SUPPORT", "COUNTER"]
        )
        
        for i, cls in enumerate(results['classifications'], 1):
            if cls.argument_type not in arg_filter:
                continue
            
            if cls.confidence < min_confidence:
                continue
            
            icon = {
                "CLAIM": "🟢",
                "SUPPORT": "🔵",
                "COUNTER": "🟣",
                "NEUTRAL": "⚪"
            }.get(cls.argument_type, "⚪")
            
            with st.container():
                col1, col2 = st.columns([0.2, 0.8])
                
                with col1:
                    st.markdown(f"### {icon}")
                
                with col2:
                    st.markdown(f"**[{i}] {cls.argument_type}**")
                    st.write(cls.sentence_text)
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Confidence", f"{cls.confidence:.0%}", label_visibility="collapsed")
                    with col_b:
                        st.metric("Strength", f"{cls.strength:.0%}", label_visibility="collapsed")
                    with col_c:
                        st.metric("Emotion", f"{cls.emotionality:.0%}", label_visibility="collapsed")
                
                st.divider()
    
    # Tab 2: Structure
    with tab2:
        st.subheader("Argument Tree Structure")
        
        tree_ascii = results['builder'].visualize_ascii()
        st.code(tree_ascii, language="text")
        
        st.subheader("Structure Statistics")
        stats = results['builder'].get_tree_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Nodes", stats['total_nodes'])
            st.metric("Max Depth", stats['max_depth'])
        with col2:
            st.metric("Root Claims", len(results['builder'].root_claims))
            st.metric("Avg Strength", f"{stats['avg_strength']:.2f}")
    
    # Tab 3: Emotions
    with tab3:
        st.subheader("Sentiment & Emotional Analysis")
        
        emotion_summary = results['emotion_summary']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("😊 Positive", emotion_summary['positive'])
        with col2:
            st.metric("😐 Neutral", emotion_summary['neutral'])
        with col3:
            st.metric("😠 Negative", emotion_summary['negative'])
        
        st.divider()
        
        # Sentiment chart
        sentiment_data = {
            "Positive": emotion_summary['positive'],
            "Neutral": emotion_summary['neutral'],
            "Negative": emotion_summary['negative']
        }
        
        st.bar_chart(sentiment_data)
        
        st.divider()
        st.metric("Avg Sentiment Score", f"{emotion_summary['avg_sentiment']:+.2f}")
        st.metric("Avg Emotionality", f"{emotion_summary['avg_emotionality']:.2f}")
    
    # Tab 4: Weaknesses
    with tab4:
        st.subheader("Detected Logical Weaknesses & Fallacies")
        
        classifier = ArgumentClassifier()
        
        weakness_count = 0
        for cls in results['classifications']:
            weaknesses = classifier.detect_logical_weaknesses(cls)
            
            has_weakness = any("⚠️" in w or "🔴" in w for w in weaknesses)
            if has_weakness:
                weakness_count += 1
                
                with st.container():
                    st.markdown(f"**📍 {cls.sentence_text}**")
                    for weakness in weaknesses:
                        if "⚠️" in weakness or "🔴" in weakness:
                            st.warning(weakness)
                    st.divider()
        
        if weakness_count == 0:
            st.success("✅ No major logical weaknesses detected!")
    
    # Tab 5: Details
    with tab5:
        st.subheader("Detailed Breakdown")
        
        # Per-argument details
        st.markdown("### Full Argument List")
        
        df_data = []
        for cls in results['classifications']:
            df_data.append({
                "Type": cls.argument_type,
                "Text": cls.sentence_text[:50] + "...",
                "Confidence": f"{cls.confidence:.0%}",
                "Strength": f"{cls.strength:.0%}",
                "Sentiment": cls.sentiment,
                "Emotionality": f"{cls.emotionality:.0%}"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        
        # Raw JSON export
        st.markdown("### Export as JSON")
        export_data = {
            "metadata": {
                "total_sentences": len(results['classifications']),
                "avg_strength": results['argument_summary']['CLAIM']['avg_strength'] if results['argument_summary']['CLAIM']['count'] > 0 else 0
            },
            "arguments": [
                {
                    "type": cls.argument_type,
                    "text": cls.sentence_text,
                    "confidence": cls.confidence,
                    "strength": cls.strength,
                    "sentiment": cls.sentiment,
                    "emotionality": cls.emotionality
                }
                for cls in results['classifications']
            ]
        }
        
        import json
        st.json(export_data)

# Footer
st.divider()
st.markdown("""
---
**🧠 Argument Structure Analyzer** | [GitHub](https://github.com) | [Documentation](README.md)
""")
