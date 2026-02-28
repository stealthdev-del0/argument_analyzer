"""
Argument Structure Analyzer - Streamlit Web App
GUI für interaktive Argument-Analyse
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Custom CSS - Light theme with proper contrast
st.markdown("""
<style>
    /* Light background, dark text */
    body {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    
    /* Text visibility */
    p, span, li, label {
        color: #262730 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1f77b4 !important;
    }
    
    /* Metric boxes */
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .stMetric label {
        color: #1f1f1f !important;
        font-weight: 700 !important;
    }
    
    /* Input fields */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #262730 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    
    .stButton button:hover {
        background-color: #1557a0 !important;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #e3f2fd !important;
        color: #1565c0 !important;
    }
    
    .stWarning {
        background-color: #fff3e0 !important;
        color: #e65100 !important;
    }
    
    .stSuccess {
        background-color: #e8f5e9 !important;
        color: #2e7d32 !important;
    }
    
    .stError {
        background-color: #ffebee !important;
        color: #c62828 !important;
    }

    /* Responsive adjustments for mobile devices */
    @media only screen and (max-width: 768px) {
        /* stack columns vertically */
        [data-testid="stColumns"] {
            flex-direction: column !important;
        }

        /* make metrics full width */
        .stMetric {
            width: 100% !important;
        }

        /* adjust text area width and height */
        textarea {
            min-height: 150px !important;
        }

        /* reduce side padding of main container */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* increase button padding for easier touch */
        .stButton button {
            padding: 0.75rem 1.25rem !important;
        }
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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📋 Arguments", "🌳 Structure", "😊 Emotions", "🔴 Weaknesses", "📈 Details", "📊 Visualizations"]
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
        
        # Sentiment chart with Plotly
        sentiment_data = {
            "Sentiment": ["Positive", "Neutral", "Negative"],
            "Count": [
                emotion_summary['positive'],
                emotion_summary['neutral'],
                emotion_summary['negative']
            ]
        }
        
        fig_sentiment = px.bar(
            sentiment_data,
            x='Sentiment',
            y='Count',
            color='Sentiment',
            color_discrete_map={
                'Positive': '#00cc96',
                'Neutral': '#636EFA',
                'Negative': '#ef553b'
            }
        )
        fig_sentiment.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Count",
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
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
    
    # Tab 6: Visualizations
    with tab6:
        st.subheader("📊 Comprehensive Visualizations")
        
        # Prepare data for visualizations
        df_analysis = pd.DataFrame([
            {
                "Type": cls.argument_type,
                "Confidence": cls.confidence,
                "Strength": cls.strength,
                "Sentiment": cls.sentiment,
                "Emotionality": cls.emotionality,
                "Text": cls.sentence_text[:30] + "..."
            }
            for cls in results['classifications']
        ])
        
        # Row 1: Pie chart and Type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Argument Type Distribution")
            type_counts = df_analysis['Type'].value_counts()
            fig_pie = go.Figure(data=[go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                marker=dict(
                    colors=['#00cc96', '#636EFA', '#ab63fa', '#cccccc'][:len(type_counts)]
                ),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            fig_pie.update_layout(
                height=350,
                showlegend=True,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 💪 Strength by Argument Type")
            fig_strength = px.box(
                df_analysis,
                x='Type',
                y='Strength',
                color='Type',
                color_discrete_map={
                    'CLAIM': '#00cc96',
                    'SUPPORT': '#636EFA',
                    'COUNTER': '#ab63fa',
                    'NEUTRAL': '#cccccc'
                },
                points='all'
            )
            fig_strength.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="",
                yaxis_title="Strength Score",
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig_strength, use_container_width=True)
        
        st.divider()
        
        # Row 2: Confidence vs Strength scatter plot
        st.markdown("#### 📍 Confidence vs Strength Analysis")
        fig_scatter = px.scatter(
            df_analysis,
            x='Confidence',
            y='Strength',
            color='Type',
            size='Emotionality',
            hover_data=['Text', 'Sentiment'],
            color_discrete_map={
                'CLAIM': '#00cc96',
                'SUPPORT': '#636EFA',
                'COUNTER': '#ab63fa',
                'NEUTRAL': '#cccccc'
            }
        )
        fig_scatter.update_layout(
            height=400,
            xaxis_title="Confidence Score",
            yaxis_title="Argument Strength",
            hovermode='closest',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.divider()
        
        # Row 3: Emotions and Sentiment metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 😊 Sentiment Distribution")
            sentiment_counts = df_analysis['Sentiment'].value_counts()
            fig_sentiment = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                labels={'x': 'Sentiment', 'y': 'Count'},
                color=sentiment_counts.index,
                color_discrete_map={
                    'POSITIVE': '#00cc96',
                    'NEUTRAL': '#636EFA',
                    'NEGATIVE': '#ef553b'
                }
            )
            fig_sentiment.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="",
                yaxis_title="Count",
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔥 Emotionality Distribution")
            fig_emotion_hist = px.histogram(
                df_analysis,
                x='Emotionality',
                nbins=15,
                color_discrete_sequence=['#ab63fa']
            )
            fig_emotion_hist.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Emotionality Score",
                yaxis_title="Frequency",
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig_emotion_hist, use_container_width=True)
        
        st.divider()
        
        # Row 4: Radar chart
        st.markdown("#### 🎯 Overall Metrics Radar")
        
        # Compute averages by type
        radar_data = df_analysis.groupby('Type')[['Confidence', 'Strength', 'Emotionality']].mean()
        
        fig_radar = go.Figure()
        
        for arg_type in radar_data.index:
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    radar_data.loc[arg_type, 'Confidence'],
                    radar_data.loc[arg_type, 'Strength'],
                    radar_data.loc[arg_type, 'Emotionality']
                ],
                theta=['Confidence', 'Strength', 'Emotionality'],
                fill='toself',
                name=arg_type
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            height=450,
            showlegend=True,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.divider()
        
        # Row 5: Summary statistics table
        st.markdown("#### 📊 Summary Statistics by Type")
        
        summary_stats = df_analysis.groupby('Type').agg({
            'Confidence': ['mean', 'min', 'max', 'std'],
            'Strength': ['mean', 'min', 'max', 'std'],
            'Emotionality': ['mean', 'min', 'max', 'std']
        }).round(3)
        
        st.dataframe(summary_stats, use_container_width=True)

# Footer
st.divider()
st.markdown("""
---
**🧠 Argument Structure Analyzer** | [GitHub](https://github.com) | [Documentation](README.md)
""")
