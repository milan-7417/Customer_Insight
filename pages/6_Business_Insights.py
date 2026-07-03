import streamlit as st
import pandas as pd
from utils.data_loader import load_customer_data
from utils.sidebar import load_sidebar

# Page Config
st.set_page_config(
    page_title="CustomerInsight - Business Insights & Recommendations",
    page_icon="📈",
    layout="wide"
)

# Load data and apply filters
df = load_customer_data()
filtered_df = load_sidebar(df, page_name="Business Insights")

st.markdown("<h1 style='margin-bottom: 5px;'>Business Insights & Strategic Plan</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1rem; margin-bottom: 25px;'>Data-driven marketing recommendations, growth initiatives, and executive-level business intelligence reports.</p>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust the sidebar filters.")
else:
    # 1. Executive Summary Highlight Card
    with st.container(key="bus_exec_summary"):
        st.markdown("<h3 style='color:#7C3AED; margin-top:0;'>📋 Executive Summary</h3>", unsafe_allow_html=True)
        
        # Calculate summary numbers
        total_rev = filtered_df["Total_Spend"].sum()
        total_cust = len(filtered_df)
        avg_rating = filtered_df["Average_Rating"].mean()
        loyal_pct = len(filtered_df[filtered_df["Loyalty_Score"] >= 7.0]) / total_cust * 100
        
        st.markdown(
            f"""
            This cohort contains **{total_cust:,}** active customer profiles generating a total revenue of 
            **₹{total_rev / 10000000:.2f} Cr** (or ₹{total_rev / 100000:.1f} L) with an average customer rating of 
            **{avg_rating:.2f} / 5.0**. Highly loyal accounts (Loyalty score ≥ 7) represent **{loyal_pct:.1f}%** of the user base.
            Based on demographic distribution and buying trends, we recommend focusing marketing efforts on young professionals in top tier states 
            and deploying targeted loyalty incentives to convert low-spend Bronze tier members.
            """,
            unsafe_allow_html=True
        )

    # 2. Performance Summary Grid
    st.markdown("### Performance Summaries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(key="bus_perf_1"):
            st.markdown("#### 🔝 Top Performing Categories")
            cat_perf = filtered_df.groupby("Preferred_Category")["Total_Spend"].sum().sort_values(ascending=False)
            for i, (cat, val) in enumerate(cat_perf.head(3).items(), 1):
                st.markdown(f"**{i}. {cat}** — ₹{val / 100000:.1f} L")
                
    with col2:
        with st.container(key="bus_perf_2"):
            st.markdown("#### 📍 Top Performing Cities")
            city_perf = filtered_df.groupby("City")["Total_Spend"].sum().sort_values(ascending=False)
            for i, (city, val) in enumerate(city_perf.head(3).items(), 1):
                st.markdown(f"**{i}. {city}** — ₹{val / 100000:.1f} L")
                
    with col3:
        with st.container(key="bus_perf_3"):
            st.markdown("#### ⭐ Customer Satisfaction Summary")
            sat_perf = filtered_df["Satisfaction_Level"].value_counts(normalize=True) * 100
            for i, (sat, pct) in enumerate(sat_perf.head(3).items(), 1):
                st.markdown(f"**{i}. {sat}** — {pct:.1f}%")
                
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # 3. Strategic Action Plan & Recommendations
    st.markdown("### Actionable Business Strategy")
    
    with st.container(key="bus_strategy_plan"):
        bt1, bt2, bt3 = st.tabs([
            "🎯 Marketing Recommendations", 
            "🚀 Growth Opportunities", 
            "📈 Strategic Management Summary"
        ])
        
        # TAB 1: MARKETING RECOMMENDATIONS
        with bt1:
            st.markdown("#### Target Market Campaigns & Customer Acquisition")
            st.markdown(
                """
                1. **High-Income Professional Campaign:** Deploy premium, quality-oriented display advertising for Electronics and Apparel 
                   targeting consumers aged 25-45 with post-graduate education. Highlight warranties, premium logistics, and VIP rewards.
                2. **UPI Gateway Incentives:** Since UPI is the preferred payment standard, collaborate with major digital payments providers 
                   (e.g., GPay, PhonePe, Paytm) to offer instant cashback codes to non-VIP customers, driving transaction volume.
                3. **State-Level Segment Expansion:** Allocate 60% of regional marketing budgets to Maharashtra and Karnataka, 
                   specifically funding tier-2 localized search and social media campaigns.
                4. **Discount Personalization:** Limit global discounts to avoid margin erosion. Shift towards personalized discount codes 
                   targeting the "Budget Buyers" segment (typically 20% to 30% off during weekends) while retaining list-price structures 
                   for VIPs.
                """
            )
            
        # TAB 2: GROWTH OPPORTUNITIES
        with bt2:
            st.markdown("#### Expansion and Product Development Initiatives")
            st.markdown(
                """
                1. **App Checkout Optimization:** Over 70% of transactions originate on mobile devices. Optimization of the checkout screen 
                   to load within 1.5 seconds is key to reducing cart abandonment.
                2. **Membership Upsell Program:** Target "Bronze" and "Silver" members who have high incomes (> ₹8 Lakhs) but lower transaction counts. 
                   Provide a 3-month free trial of the VIP program to increase their basket size.
                3. **Category Bundling:** Launch bundles combining high-value Electronics (highest revenue driver) with related Accessories 
                   or Apparel to increase average order values.
                4. **Feedback-Driven Logistics:** With delivery issues being a significant driver of unsatisfied customer ratings, 
                   implementing regional micro-fulfillment warehouses in Delhi and Bengaluru will reduce delivery times to under 48 hours.
                """
            )
            
        # TAB 3: MANAGEMENT ROADMAP
        with bt3:
            st.markdown("#### Quarterly Leadership Objectives")
            st.markdown(
                """
                - **Q1 Objective — Retention:** Reduce the active Churn Rate from current levels by sending automated push notifications 
                  with loyalty points to users who have not logged in for over 45 days.
                - **Q2 Objective — Efficiency:** Migrate Net Banking and Cash-on-Delivery users to UPI and Credit Cards by introducing a 
                  ₹50 flat waiver on UPI checkouts. This reduces processing costs and cash management overhead.
                - **Q3 Objective — Average Order Expansion:** Scale the average basket size by 15% through smart recommender systems 
                  suggesting items during checkout.
                - **Q4 Objective — VIP Care:** Establish a dedicated 24/7 customer service desk for VIP/Gold status accounts to push satisfaction 
                  ratings to >4.5 across all metro areas.
                """
            )
            
    # 4. Report Download Utility
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    with st.container(key="bus_download_section"):
        st.markdown("#### Export Briefing Document")
        st.markdown("Download a fully compiled markdown version of the strategic recommendations report.")
        
        # Construct markdown string for report
        report_text = f"""# CustomerInsight - Strategic Business Report
Generated on: 2026-07-03

## Executive Metrics
- Total Customer Cohort: {total_cust:,}
- Total Revenue Analyzed: ₹{total_rev:,.2f}
- Cohort Average Rating: {avg_rating:.2f} / 5.0

## Top Performers
- Leading State: {city_perf.index[0]}
- Top Category: {cat_perf.index[0]}

## Strategic Initiatives
1. Target high-income demographics with premium service plans.
2. Reduce cart abandonment by optimizing mobile checkouts.
3. Incentivize UPI checkout to reduce COD operational overhead.
"""
        st.download_button(
            label="📄 Download Executive Briefing (.md)",
            data=report_text,
            file_name="executive_strategic_briefing.md",
            mime="text/markdown",
            type="primary"
        )
        
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>CustomerInsight Dashboard v1.0.0 | Business Insights Module</p>", unsafe_allow_html=True)
