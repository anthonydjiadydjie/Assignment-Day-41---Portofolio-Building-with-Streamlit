import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Social Media Engagement Analysis",
    layout="wide"
)

st.title("📊 Social Media Engagement Analysis")
st.markdown("""
**Name:** Anthony Djiady Djie  
**Class:** DS39+  
**Topic:** EC 3 (Social Media Engagement)
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join("data", "social_media_engagement.csv"))

    return df

df = load_data()

# ----------------------------
# Dataset Overview
# ----------------------------
st.header("📁 Dataset Overview")

st.subheader("Preview Data")
st.dataframe(df.head())

st.subheader("Dataset Information")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

st.subheader("Descriptive Statistics")
st.dataframe(df.describe())

st.subheader("Missing Values")
st.dataframe(df.isnull().sum())

# ----------------------------
# Data Cleaning
# ----------------------------
st.header("🧹 Data Cleaning")

numeric_cols = ['likes_count', 'comments_count', 'shares_count', 'impressions']

for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

st.success("Missing values in numeric columns have been handled")

# ----------------------------
# Feature Engineering
# ----------------------------
st.header("📐 Engagement Metrics")

# Interactions
df['interactions'] = (
    df['likes_count'] +
    df['comments_count'] +
    df['shares_count']
)

# Interaction per Impression
df['interaction_per_impression'] = (
    df['interactions'] / df['impressions']
) * 100

st.subheader("Calculated Metrics (Preview)")
st.dataframe(
    df[['likes_count', 'comments_count', 'shares_count',
        'interactions', 'interaction_per_impression']].head()
)

# ----------------------------
# Metric Summary
# ----------------------------
st.header("📌 Metrics Summary")

col1, col2 = st.columns(2)

col1.metric(
    "Average Engagement Rate",
    f"{df['engagement_rate'].mean():.2f}%"
)

col2.metric(
    "Average Interaction per Impression",
    f"{df['interaction_per_impression'].mean():.2f}%"
)

# ----------------------------
# Visualization
# ----------------------------
st.header("📊 Visual Analysis")

metric_choice = st.selectbox(
    "Select metric to visualize:",
    ['engagement_rate', 'interaction_per_impression']
)

bin_size = st.slider(
    "Select number of bins:",
    min_value=10,
    max_value=60,
    value=30,
    step=5
)

show_kde = st.checkbox("Show KDE curve", value=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(
    df[metric_choice],
    bins=bin_size,
    kde=show_kde,
    ax=ax
)

ax.set_title(f"Distribution of {metric_choice}")
ax.set_xlabel(metric_choice)
ax.set_ylabel("Frequency")

st.pyplot(fig)

# ----------------------------
# Insight Section
# ----------------------------
st.header("🧠 Key Insights")

st.markdown(f"""
- The **average engagement rate** is **{df['engagement_rate'].mean():.2f}%**, indicating the overall audience response to the content.
- The **interaction per impression** metric shows how efficiently impressions are converted into active interactions.
- Posts with higher interaction-per-impression values indicate stronger content relevance despite similar exposure levels.
""")

# ----------------------------
# Download Processed Data
# ----------------------------
st.header("⬇️ Download Processed Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="social_media_engagement_processed.csv",
    mime="text/csv"
)
