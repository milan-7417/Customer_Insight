import os
import streamlit as st
from utils.data_loader import load_customer_data
from utils.sidebar import load_sidebar

# Configure Streamlit page
st.set_page_config(
    page_title="CustomerInsight - Home",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global dataset
df = load_customer_data()

# Load sidebar and apply filters (returns filtered dataframe, though homepage displays overall snapshot)
filtered_df = load_sidebar(df, page_name="Home")

# Main content
# Hero section
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("<span style='background-color:#E9D5FF; color:#7C3AED; font-weight:600; padding:6px 12px; border-radius:20px; font-size:0.85rem;'>BUSINESS INTELLIGENCE PLATFORM</span>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin-top: 15px; margin-bottom: 20px; font-size: 3rem;'>Unlock Deep Customer Insights & Drive Growth</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size: 1.15rem; line-height: 1.6; color: #475569; margin-bottom: 30px;'>
        CustomerInsight is a modern enterprise intelligence platform designed to transform complex transactional data 
        into clear, actionable business strategies. Monitor user demographics, track purchase behaviors, analyze spending patterns, 
        and discover automated customer segments to deliver highly targeted product offerings.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # CTA Buttons
    st.markdown("### Begin Your Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.page_link("pages/1_Executive_Dashboard.py", label="Executive Dashboard", icon="📊")
    with c2:
        st.page_link("pages/5_Customer_Insights.py", label="Customer Segmentation", icon="🧠")

with col2:
    hero_path = "assets/hero.png"
    if os.path.exists(hero_path):
        st.image(hero_path, use_container_width=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Overview metrics snap-shot
st.markdown("## Platform Snapshot")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    with st.container(key="home_kpi_1"):
        st.metric(label="Total Customer Base", value=f"{len(df):,}")
        st.markdown("<p style='font-size:0.8rem; color:#64748B; margin-top:5px;'>Active profiles analyzed</p>", unsafe_allow_html=True)

with kpi2:
    with st.container(key="home_kpi_2"):
        total_rev_cr = df['Total_Spend'].sum() / 10000000.0  # Convert to Crores INR
        st.metric(label="Total Revenue generated", value=f"₹{total_rev_cr:.2f} Cr")
        st.markdown("<p style='font-size:0.8rem; color:#64748B; margin-top:5px;'>Cumulative purchase value</p>", unsafe_allow_html=True)

with kpi3:
    with st.container(key="home_kpi_3"):
        avg_rating = df['Average_Rating'].mean()
        st.metric(label="Average Customer Rating", value=f"{avg_rating:.2f} / 5.0")
        st.markdown("<p style='font-size:0.8rem; color:#64748B; margin-top:5px;'>Overall feedback score</p>", unsafe_allow_html=True)

with kpi4:
    with st.container(key="home_kpi_4"):
        repeat_cust = len(df[df['Monthly_Orders_Avg'] >= 3.0]) / len(df) * 100
        st.metric(label="Loyal Repeat Buyers", value=f"{repeat_cust:.1f}%")
        st.markdown("<p style='font-size:0.8rem; color:#64748B; margin-top:5px;'>Frequent monthly ordering rate</p>", unsafe_allow_html=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Module/Feature Cards
st.markdown("## Analytical Modules")

fc1, fc2, fc3 = st.columns(3, gap="medium")

with fc1:
    with st.container(key="feat_1"):
        st.markdown("### 📊 Executive Dashboard")
        st.markdown("Track overall corporate KPIs, cumulative metrics, order trends, distribution breakdowns, and performance across top metrics.")
        st.page_link("pages/1_Executive_Dashboard.py", label="Open Executive View", icon="👉")

with fc2:
    with st.container(key="feat_2"):
        st.markdown("### 👥 Customer Demographics")
        st.markdown("Analyze patterns across age bands, gender classifications, education stages, occupation types, and geographical concentrations.")
        st.page_link("pages/2_Customer_Demographics.py", label="Explore Demographics", icon="👉")

with fc3:
    with st.container(key="feat_3"):
        st.markdown("### 🛒 Purchase Behavior")
        st.markdown("Gain understanding on purchase frequency, payment mode preferences, discount reactions, cart abandonment, and timing details.")
        st.page_link("pages/3_Purchase_Behavior.py", label="Study Purchase Behavior", icon="👉")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

fc4, fc5, fc6 = st.columns(3, gap="medium")

with fc4:
    with st.container(key="feat_4"):
        st.markdown("### 💰 Spending Analysis")
        st.markdown("Analyze income brackets, average basket sizes, category performance, regional spending, and identify high-value consumer groups.")
        st.page_link("pages/4_Spending_Analysis.py", label="Run Spending Analysis", icon="👉")

with fc5:
    with st.container(key="feat_5"):
        st.markdown("### 🧠 Customer Insights & Analysis")
        st.markdown("Review feedback trends, churn risks, and run K-Means algorithms to construct automatic customer segments and personas.")
        st.page_link("pages/5_Customer_Insights.py", label="Open Customer Insights", icon="👉")

with fc6:
    with st.container(key="feat_6"):
        st.markdown("### 📈 Business Insights")
        st.markdown("Export a compiled summary report with strategic suggestions, marketing opportunities, and growth directions.")
        st.page_link("pages/6_Business_Insights.py", label="Get Recommendations", icon="👉")

# Footer
st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>CustomerInsight Dashboard v1.0.0 | Developed as a production-grade Business Intelligence portal.</p>", unsafe_allow_html=True)
