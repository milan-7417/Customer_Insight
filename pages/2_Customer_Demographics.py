import streamlit as st
import pandas as pd
from utils.data_loader import load_customer_data
from utils.sidebar import load_sidebar
from utils.charts import histogram_chart, donut_chart, bar_chart, treemap_chart, horizontal_bar_chart

# Page Config
st.set_page_config(
    page_title="CustomerInsight - Customer Demographics",
    page_icon="👥",
    layout="wide"
)

# Load data and apply filters
df = load_customer_data()
filtered_df = load_sidebar(df, page_name="Customer Demographics")

st.markdown("<h1 style='margin-bottom: 5px;'>Customer Demographics</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1rem; margin-bottom: 25px;'>Demographic profile details including age brackets, occupational tiers, and geographic segmentation.</p>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust the sidebar filters.")
else:
    # Row 1: Age Distribution & Gender Share
    r1c1, r1c2 = st.columns([3, 2], gap="medium")
    
    with r1c1:
        with st.container(key="demo_chart_1"):
            fig_age = histogram_chart(filtered_df, x="Age", title="Age Distribution of Customers", nbins=20)
            st.plotly_chart(fig_age, use_container_width=True)
            
    with r1c2:
        with st.container(key="demo_chart_2"):
            gender_df = filtered_df['Gender'].value_counts().reset_index()
            gender_df.columns = ["Gender", "Count"]
            fig_gender = donut_chart(gender_df, names="Gender", values="Count", title="Gender Distribution")
            st.plotly_chart(fig_gender, use_container_width=True)
            
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 2: Education & Occupation Analysis
    r2c1, r2c2 = st.columns([1, 1], gap="medium")
    
    with r2c1:
        with st.container(key="demo_chart_3"):
            edu_df = filtered_df['Education'].value_counts().reset_index()
            edu_df.columns = ["Education Level", "Customers"]
            fig_edu = bar_chart(edu_df, x="Education Level", y="Customers", title="Education Level Distribution")
            st.plotly_chart(fig_edu, use_container_width=True)
            
    with r2c2:
        with st.container(key="demo_chart_4"):
            occ_df = filtered_df['Occupation'].value_counts().reset_index()
            occ_df.columns = ["Occupation", "Customers"]
            fig_occ = bar_chart(occ_df, x="Occupation", y="Customers", title="Occupation Distribution")
            st.plotly_chart(fig_occ, use_container_width=True)
            
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 3: State & City Treemap (Hierarchical Geography)
    with st.container(key="demo_chart_5"):
        geo_df = filtered_df.groupby(["State", "City"]).size().reset_index(name="Customers")
        fig_treemap = treemap_chart(geo_df, path=["State", "City"], values="Customers", title="Geographical Hierarchy: State and City Representation")
        st.plotly_chart(fig_treemap, use_container_width=True)
        
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 4: Membership Tier Distribution & Insights
    r4c1, r4c2 = st.columns([2, 3], gap="medium")
    
    with r4c1:
        with st.container(key="demo_chart_6"):
            mem_df = filtered_df['Membership_Type'].value_counts().reset_index()
            mem_df.columns = ["Membership Tier", "Customers"]
            # Fill NA values as None
            mem_df["Membership Tier"] = mem_df["Membership Tier"].fillna("None")
            fig_mem = donut_chart(mem_df, names="Membership Tier", values="Customers", title="Membership Tier Distribution")
            st.plotly_chart(fig_mem, use_container_width=True)
            
    with r4c2:
        with st.container(key="demo_insights"):
            st.markdown("### 👥 Demographic Insights")
            
            # Demographic summaries
            mode_age = filtered_df['Age'].mode()[0]
            mode_occ = occ_df.iloc[0]['Occupation']
            mode_edu = edu_df.iloc[0]['Education Level']
            mode_state = geo_df.groupby('State')['Customers'].sum().idxmax()
            
            st.markdown(
                f"""
                - **Target Age Segment:** The customer base peaks around young to middle-aged professionals, with the most common age being 
                  **{mode_age} years old**. A substantial portion of the customer base falls between 25 and 45 years of age.
                - **Gender representation:** The split is fairly equal between Male and Female customers, allowing broad general-interest marketing campaigns.
                - **Professional Profiles:** **{mode_occ}s** represent the largest occupational segment, representing a demographic with high e-commerce familiarity and buying power.
                - **Academic backgrounds:** Most shoppers hold a **{mode_edu}** degree, indicating an educated user group that likely researches products before purchase.
                - **Tier Distribution:** Gold and Bronze tiers hold a significant share of users. Upgrading "Bronze" and "None" members represents a major loyalty campaign opportunity.
                - **Geographic Focus:** The state of **{mode_state}** leads customer counts. Expansion into tier-2 cities within this state is highly recommended.
                """,
                unsafe_allow_html=True
            )
            
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>CustomerInsight Dashboard v1.0.0 | Customer Demographics Module</p>", unsafe_allow_html=True)
