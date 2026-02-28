# 📊 Graphical Visualizations Guide

## Overview

The **Argument Structure Analyzer** now includes comprehensive graphical visualizations to help you analyze argumentative structures visually.

---

## New Features

### 1. **Edit Tab 3: Enhanced Sentiment Chart** 😊
- **Plotly Bar Chart** showing sentiment distribution (Positive, Neutral, Negative)
- Interactive hover tooltips
- Color-coded by sentiment type
- Improved over basic Streamlit bar chart

### 2. **New Tab 6: Comprehensive Visualizations Dashboard** 📊

A completely new "Visualizations" tab with 5 advanced charts:

#### A. **Argument Type Distribution** (Pie Chart)
- Shows proportion of Claims, Supports, Counters, and Neutral arguments
- Interactive labels with percentages
- Click to highlight segments

#### B. **Strength by Argument Type** (Box Plot)
- Displays distribution of argument strength across argument types
- Shows min, max, median, and quartiles
- Includes all individual data points (scatter)
- Helps identify which argument types tend to be stronger

#### C. **Confidence vs Strength** (Scatter Plot)
- X-axis: Confidence scores
- Y-axis: Strength scores
- Bubble size: Emotionality level
- Color: Argument type
- Hover: See full text and sentiment
- Identifies high-confidence, high-strength arguments

#### D. **Sentiment Distribution** (Bar Chart)
- Count of Positive, Neutral, and Negative arguments
- Color-coded bars
- Helps assess overall text sentiment polarity

#### E. **Emotionality Distribution** (Histogram)
- Shows frequency distribution of emotionality scores
- 15 bins for granular insights
- Identifies how "emotional" your text is

#### F. **Metrics Radar Chart**
- Multi-dimensional comparison of:
  - Confidence
  - Strength
  - Emotionality
- One trace per argument type
- Shows patterns that distinguish argument types

#### G. **Summary Statistics Table**
- Detailed statistics by argument type:
  - Mean, Min, Max, Std Dev
  - For Confidence, Strength, and Emotionality
- Exportable data for further analysis

---

## How to Use

### Running the App
```bash
cd /Users/Salomo/Desktop/Programmier_Projekt/argument_analyzer
./start.sh
```

Then navigate to `http://localhost:8501` in your browser.

### Viewing Visualizations

1. **Analyze text** using the input section
2. **Click "Analyze"** button
3. **Navigate to "📊 Visualizations" tab** (the 6th tab)

### Interactive Features

All Plotly charts are **fully interactive**:
- **Hover**: See detailed information about data points
- **Zoom**: Click and drag to zoom into specific regions
- **Pan**: Hold shift and drag to pan around
- **Legend**: Click legend items to show/hide traces
- **Download**: Use the camera icon to save chart as PNG

---

## Example Insights

### From Pie Chart
- **Use case**: Quickly see if your text is mostly claims or supporting evidence
- **Good ratio**: Balanced mix of claims, supports, and counters

### From Scatter Plot
- **Use case**: Find your strongest, most confident arguments
- **Look for**: Upper-right quadrant (high confidence + high strength)
- **Bubble size**: Emotional arguments for persuasive impact

### From Radar Chart
- **Use case**: Compare argument types at a glance
- **Pattern recognition**: Identify if one type consistently scores higher

### From Box Plots
- **Use case**: Understand typical strength of each argument type
- **Outliers**: See unusual strong/weak arguments

---

## Technical Details

### Libraries Used
- **Plotly Express**: High-level charting API
- **Plotly Graph Objects**: Low-level graph customization
- **Pandas**: Data aggregation and statistics

### Chart Customization
All charts feature:
- ✅ Light theme (readable text)
- ✅ Consistent color scheme
- ✅ Mobile-responsive sizing
- ✅ Custom hover templates
- ✅ Proper margins and spacing

---

## Requirements

Ensure `plotly>=5.0.0` is installed:

```bash
pip install plotly>=5.0.0
```

Or use the included startup script which automatically installs dependencies.

---

## Future Enhancements

Potential additions:
- 🔄 Time-series charts (if analyzing multiple texts)
- 🌐 Network graph visualization of argument relationships
- 📈 Trend analysis across multiple analyses
- 🎨 Custom color scheme preferences
- 💾 Export visualizations as static images/PDFs

---

**Happy analyzing!** 🚀
