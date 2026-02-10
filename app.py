import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io

# =========================
# PAGE CONFIG (MUST BE FIRST)
# =========================
st.set_page_config(
    page_title="Social Media Engagement Analysis",
    layout="wide"
)

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("Pengaturan & Navigasi")

page = st.sidebar.radio(
    "Pilih Halaman:",
    ["Profil", "Dashboard"]
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join("data", "social_media_engagement.csv"))

df = load_data()

# =========================
# PAGE 1: PROFIL
# =========================
if page == "Profil":
    st.title("Tentang Saya")

    st.subheader("Siapa Anthony?")
    st.write(
        """
        Halo! Saya **Anthony Djiady Djie**,  
        seorang Data Science Bootcamp student di **Dibimbing.id** yang sedang
        membangun portfolio menggunakan **Streamlit**.

        Project ini dibuat untuk menganalisis **Social Media Engagement**
        secara interaktif dan mudah dipahami oleh pengguna non-teknis.
        """
    )

    st.markdown("---")

    st.subheader("Project Info")
    st.write("""
    - **Topik**: Social Media Engagement  
    - **Class**: DS39+ Dibimbing.id  
    - **Tools**: Python, Pandas, Streamlit  
    """)

# =========================
# PAGE 2: DASHBOARD
# =========================
elif page == "Dashboard":
    st.title("📊 Social Media Engagement Analysis")

    st.markdown("""
    **Name:** Anthony Djiady Djie  
    **Class:** DS39+  
    **Topic:** EC 3 (Social Media Engagement)
    """)

    # ----------------------------
    # DATASET OVERVIEW
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
    # DATA CLEANING
    # ----------------------------
    st.header("🧹 Data Cleaning")

    numeric_cols = [
        'likes_count',
        'comments_count',
        'shares_count',
        'impressions'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    st.success("Missing values in numeric columns have been handled")

    # ----------------------------
    # FEATURE ENGINEERING
    # ----------------------------
    st.header("📐 Engagement Metrics")

    df['interactions'] = (
        df['likes_count'] +
        df['comments_count'] +
        df['shares_count']
    )

    df['interaction_per_impression'] = (
        df['interactions'] / df['impressions']
    ) * 100

    st.subheader("Calculated Metrics (Preview)")
    st.dataframe(
        df[['likes_count', 'comments_count', 'shares_count',
            'interactions', 'interaction_per_impression']].head()
    )

    # ----------------------------
    # METRIC SUMMARY
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
    # VISUALIZATION
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
    # INSIGHTS
    # ----------------------------
    st.header("🧠 Key Insights")

    st.markdown(f"""
    - The **average engagement rate** is **{df['engagement_rate'].mean():.2f}%**, showing overall audience response.
    - **Interaction per impression** highlights how efficiently impressions convert into interactions.
    - Higher interaction-per-impression values indicate stronger content relevance.
    """)

    # ----------------------------
    # DOWNLOAD DATA
    # ----------------------------
    st.header("⬇️ Download Processed Dataset")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="social_media_engagement_processed.csv",
        mime="text/csv"
    )
    st.markdown("Click the button above to download the processed dataset.")
