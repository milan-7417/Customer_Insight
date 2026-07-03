import streamlit as st
import pandas as pd
from utils.data_loader import load_customer_data
from utils.sidebar import load_sidebar
from utils.charts import bar_chart, histogram_chart, scatter_chart, sunburst_chart, donut_chart

# Page Config
st.set_page_config(
    page_title="CustomerInsight - Purchase Behavior",
    page_icon="🛒",
    layout="wide"
)

# Load data and apply filters
df = load_customer_data()
filtered_df = load_sidebar(df, page_name="Purchase Behavior")

st.markdown("<h1 style='margin-bottom: 5px;'>Purchase Behavior</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1rem; margin-bottom: 25px;'>Deep dive into purchasing habits, including transaction frequency, order values, discount behavior, and device-time preferences.</p>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust the sidebar filters.")
else:
    # Row 1: Purchase Frequency & Order Value Distribution
    r1c1, r1c2 = st.columns([1, 1], gap="medium")
    
    with r1c1:
        with st.container(key="purchase_chart_1"):
            freq_df = filtered_df['Purchase_Frequency'].value_counts().reset_index()
            freq_df.columns = ["Purchase Frequency", "Customers"]
            # Sort order: Daily, Weekly, Monthly, Occasional
            freq_order = {"Daily": 0, "Weekly": 1, "Monthly": 2, "Occasional": 3}
            freq_df["sort_order"] = freq_df["Purchase Frequency"].map(freq_order)
            freq_df = freq_df.sort_values(by="sort_order").drop(columns="sort_order")
            
            fig_freq = bar_chart(freq_df, x="Purchase Frequency", y="Customers", title="Purchase Frequency Distribution")
            st.plotly_chart(fig_freq, use_container_width=True)
            
    with r1c2:
        with st.container(key="purchase_chart_2"):
            fig_aov_dist = histogram_chart(filtered_df, x="Average_Order_Value", title="Average Order Value (AOV) Distribution", nbins=30)
            st.plotly_chart(fig_aov_dist, use_container_width=True)
            
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 2: Monthly Orders Avg & Payment Methods Share
    r2c1, r2c2 = st.columns([1, 1], gap="medium")
    
    with r2c1:
        with st.container(key="purchase_chart_3"):
            fig_mo = histogram_chart(filtered_df, x="Monthly_Orders_Avg", title="Average Monthly Orders per Customer", nbins=15)
            st.plotly_chart(fig_mo, use_container_width=True)
            
    with r2c2:
        with st.container(key="purchase_chart_4"):
            pay_df = filtered_df['Payment_Method'].value_counts().reset_index()
            pay_df.columns = ["Payment Method", "Count"]
            fig_pay = donut_chart(pay_df, names="Payment Method", values="Count", title="Payment Method Share")
            st.plotly_chart(fig_pay, use_container_width=True)
            
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 3: Category Preference by Gender
    with st.container(key="purchase_chart_5"):
        cat_gender = filtered_df.groupby(["Preferred_Category", "Gender"]).size().reset_index(name="Customers")
        fig_cat_gender = bar_chart(cat_gender, x="Preferred_Category", y="Customers", color="Gender", barmode="group", title="Category Preferences Split by Gender")
        st.plotly_chart(fig_cat_gender, use_container_width=True)
        
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 4: Discount Analysis & Sunburst Purchase Trends
    r4c1, r4c2 = st.columns([1, 1], gap="medium")
    
    with r4c1:
        with st.container(key="purchase_chart_6"):
            # Discount ratio vs Total spend
            fig_disc = scatter_chart(
                filtered_df, 
                x="Discount_Applied_Ratio", 
                y="Total_Spend", 
                color="Membership_Type", 
                title="Discount Applied Ratio vs. Total Spend (by Membership)"
            )
            st.plotly_chart(fig_disc, use_container_width=True)
            
    with r4c2:
        with st.container(key="purchase_chart_7"):
            # Sunburst hierarchy: Preferred purchase time -> device preference
            trend_hier = filtered_df.groupby(["Preferred_Purchase_Time", "Device_Preference"]).size().reset_index(name="Transactions")
            fig_sunburst = sunburst_chart(
                trend_hier, 
                path=["Preferred_Purchase_Time", "Device_Preference"], 
                values="Transactions", 
                title="Purchase Trends: Time of Day and Device Share"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
            
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Row 5: Business Insights
    with st.container(key="purchase_insights"):
        st.markdown("### 🛒 Purchase Behavior Insights")
        
        mode_time = filtered_df['Preferred_Purchase_Time'].mode()[0]
        mode_device = filtered_df['Device_Preference'].mode()[0]
        mode_payment = pay_df.iloc[0]['Payment Method']
        
        st.markdown(
            f"""
            - **Order Patterns:** The majority of customers order on a **Weekly** or **Monthly** basis. Regular engagement campaigns 
              can help push "Monthly" users into the "Weekly" segment.
            - **Transaction Valuations:** Average order values show a peak in the ₹1,000 to ₹5,000 range. Premium VIP members shift the 
              distribution with purchases reaching up to ₹15,000.
            - **Discount Responsiveness:** The scatter analysis reveals a positive correlation between discount frequency and total spending, 
              especially for **Bronze** and **None** tier members. VIP and Gold members show less sensitivity, indicating opportunities 
              for non-discount-based value propositions (e.g. priority shipping, early product access).
            - **Shopping Channels:** Operations are heavily mobile-skewed, with **{mode_device}** transactions dominating. 
              Engineering teams must prioritize app stability and speed.
            - **Peak Buying Hours:** Most shopping happens during the **{mode_time}**. Marketing push notifications should be 
              scheduled during these windows to maximize open and conversion rates.
            - **Payment Trends:** Modern payment modes, led by **{mode_payment}**, represent the vast majority of checkouts, indicating 
              the importance of zero-friction UPI links.
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>CustomerInsight Dashboard v1.0.0 | Purchase Behavior Module</p>", unsafe_allow_html=True)
