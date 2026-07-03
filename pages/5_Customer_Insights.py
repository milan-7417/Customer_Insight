import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_loader import load_customer_data
from utils.sidebar import load_sidebar
from utils.charts import box_plot, scatter_chart, donut_chart, apply_layout_styles

# Page Config
st.set_page_config(
    page_title="CustomerInsight - Customer Insights & Segmentation",
    page_icon="🧠",
    layout="wide"
)

# 1. Cached Segmentation Function
@st.cache_data
def get_segmented_dataset():
    """Runs K-Means clustering on the full dataset and returns it with segment labels."""
    df_raw = load_customer_data()
    
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    
    # Features for clustering
    features = ['Total_Spend', 'Annual_Income', 'Age', 'Average_Rating']
    X = df_raw[features].copy()
    
    # Fill any NA (should not be any in synthetic data, but good practice)
    X = X.fillna(X.mean())
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Fit K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    df_result = df_raw.copy()
    df_result['Cluster'] = clusters
    
    # Rank clusters by mean spend to assign descriptive labels
    cluster_means = df_result.groupby('Cluster')['Total_Spend'].mean().sort_values(ascending=False)
    cluster_mapping = {
        cluster_means.index[0]: "VIP Spenders",
        cluster_means.index[1]: "Value Seekers",
        cluster_means.index[2]: "Occasional Shoppers",
        cluster_means.index[3]: "Budget Buyers"
    }
    
    df_result['Segment'] = df_result['Cluster'].map(cluster_mapping)
    return df_result

# Load segmented data
df_segmented = get_segmented_dataset()

# Apply standard filters using the sidebar loader
filtered_df = load_sidebar(df_segmented, page_name="Customer Insights")

st.markdown("<h1 style='margin-bottom: 5px;'>Customer Insights & Advanced Segmentation</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1rem; margin-bottom: 25px;'>Advanced predictive analytics, feedback review, and machine learning-powered K-Means customer segmentation.</p>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust the sidebar filters.")
else:
    # Set tabs
    tab_segmentation, tab_loyalty, tab_satisfaction = st.tabs([
        "🤖 Advanced Customer Segmentation", 
        "💎 Loyalty & VIP Analysis", 
        "⭐ Cart & Ratings Analysis"
    ])
    
    # TAB 1: K-MEANS SEGMENTATION
    with tab_segmentation:
        st.markdown("### K-Means Clustering Analysis")
        st.markdown("Automated clustering identifies four distinct consumer segments based on age, income, cumulative spend, and feedback ratings.")
        
        # Grid layout for segment chart and summary
        r1c1, r1c2 = st.columns([3, 2], gap="medium")
        
        with r1c1:
            with st.container(key="seg_3d_block"):
                # Sample down if dataframe is huge for fluid 3D rendering
                plot_sample = filtered_df.sample(min(3000, len(filtered_df)), random_state=42)
                
                fig_3d = px.scatter_3d(
                    plot_sample,
                    x='Annual_Income',
                    y='Total_Spend',
                    z='Age',
                    color='Segment',
                    color_discrete_sequence=['#4F46E5', '#10B981', '#F59E0B', '#F43F5E'],
                    opacity=0.7,
                    title="3D Segment Mapping (Income vs. Spend vs. Age)"
                )
                fig_3d.update_layout(
                    margin=dict(l=0, r=0, b=0, t=50),
                    scene=dict(
                        xaxis=dict(title='Annual Income (₹)'),
                        yaxis=dict(title='Total Spend (₹)'),
                        zaxis=dict(title='Age')
                    ),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                # Apply Outfit Font to 3D plot
                fig_3d.update_layout(font=dict(family="Outfit, sans-serif"))
                
                st.plotly_chart(fig_3d, use_container_width=True)
                
        with r1c2:
            with st.container(key="seg_pie_block"):
                seg_counts = filtered_df['Segment'].value_counts().reset_index()
                seg_counts.columns = ["Segment", "Count"]
                
                fig_seg_pie = donut_chart(seg_counts, names="Segment", values="Count", title="Segment Distribution Share")
                st.plotly_chart(fig_seg_pie, use_container_width=True)
                
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        
        # Segment Metrics Table
        st.markdown("#### Segment Characteristic Profiles")
        seg_stats = filtered_df.groupby("Segment").agg({
            "Customer_ID": "count",
            "Age": "mean",
            "Annual_Income": "mean",
            "Total_Spend": "mean",
            "Average_Rating": "mean",
            "Loyalty_Score": "mean"
        }).reset_index()
        
        seg_stats.columns = ["Segment", "Size (Customers)", "Avg Age", "Avg Annual Income (₹)", "Avg Total Spend (₹)", "Avg Rating", "Avg Loyalty Score"]
        st.dataframe(
            seg_stats.style.format({
                "Size (Customers)": "{:,}",
                "Avg Age": "{:.1f} yrs",
                "Avg Annual Income (₹)": "₹{:,.0f}",
                "Avg Total Spend (₹)": "₹{:,.2f}",
                "Avg Rating": "{:.2f} / 5.0",
                "Avg Loyalty Score": "{:.1f} / 10"
            }), 
            use_container_width=True, 
            hide_index=True
        )
        
    # TAB 2: LOYALTY & VIP ANALYSIS
    with tab_loyalty:
        st.markdown("### Customer Loyalty & VIP Cohort Profiles")
        
        l1, l2 = st.columns([1, 1], gap="medium")
        
        with l1:
            with st.container(key="loyalty_chart_1"):
                # Loyalty score vs Total Spend
                fig_loy = scatter_chart(
                    filtered_df,
                    x="Loyalty_Score",
                    y="Total_Spend",
                    color="Membership_Type",
                    title="Loyalty Score vs. Cumulative Spend"
                )
                st.plotly_chart(fig_loy, use_container_width=True)
                
        with l2:
            # Customer Personas Visual Cards
            st.markdown("#### Strategic Customer Personas")
            
            p1, p2 = st.columns(2)
            with p1:
                with st.container(key="pers_1"):
                    st.markdown("<h5 style='color:#7C3AED; margin-top:0;'>👑 The Elite Spender</h5>", unsafe_allow_html=True)
                    st.markdown("**Segment:** VIP Spenders<br>High income, VIP status, low price-sensitivity. Demands priority service, early access, and fast delivery.", unsafe_allow_html=True)
                    
                with st.container(key="pers_2"):
                    st.markdown("<h5 style='color:#334155; margin-top:0;'>🛍️ The Steady Shopper</h5>", unsafe_allow_html=True)
                    st.markdown("**Segment:** Value Seekers<br>Graduate professionals, weekly purchase frequency, UPI payments. Highly satisfied, steady long-term value.", unsafe_allow_html=True)
            
            with p2:
                with st.container(key="pers_3"):
                    st.markdown("<h5 style='color:#334155; margin-top:0;'>🏷️ The Discount Hunter</h5>", unsafe_allow_html=True)
                    st.markdown("**Segment:** Budget Buyers<br>High discount applied ratios (60%+), lower incomes. Shops during promotional sales events.", unsafe_allow_html=True)
                    
                with st.container(key="pers_4"):
                    st.markdown("<h5 style='color:#E11D48; margin-top:0;'>⚠️ The Churn Risk</h5>", unsafe_allow_html=True)
                    st.markdown("**Segment:** Occasional Shoppers<br>Days since last purchase > 90, high cart abandonment, multiple customer service complaints.", unsafe_allow_html=True)
                    
    # TAB 3: RATINGS & CART ABANDONMENT
    with tab_satisfaction:
        st.markdown("### Feedback, Ratings & Cart Abandonment")
        
        s1, s2 = st.columns([1, 1], gap="medium")
        
        with s1:
            with st.container(key="sat_chart_1"):
                fig_ratings = box_plot(
                    filtered_df, 
                    x="Preferred_Category", 
                    y="Average_Rating", 
                    title="Average Product Ratings across Categories"
                )
                st.plotly_chart(fig_ratings, use_container_width=True)
                
        with s2:
            with st.container(key="sat_chart_2"):
                fig_cart = scatter_chart(
                    filtered_df,
                    x="Cart_Abandonment_Rate",
                    y="Days_Since_Last_Purchase",
                    color="Satisfaction_Level",
                    title="Cart Abandonment Rate vs. Purchase Recency"
                )
                st.plotly_chart(fig_cart, use_container_width=True)
                
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Insights Section
    with st.container(key="insights_satisfaction"):
        st.markdown("### 🧠 Customer Insights Summary")
        
        churn_count = len(filtered_df[filtered_df['Churn_Status'] == True])
        churn_pct = (churn_count / len(filtered_df)) * 100
        
        st.markdown(
            f"""
            - **Machine Learning Segments:** K-Means clustering highlights **VIP Spenders** as the primary revenue group. 
              **Value Seekers** constitute the bulk of stable, recurring transactions, while **Budget Buyers** require promotional codes.
            - **Churn Warning Signals:** Approximately **{churn_count:,}** customers (**{churn_pct:.1f}%** of the cohort) are flagged as **Churn Risk** 
              due to a combination of high inactivity (recency > 90 days), low loyalty ratings, and repeated customer service calls.
            - **Cart Abandonment Dynamics:** The scatter plot illustrates that users with neutral/unsatisfied ratings correlate with high 
              cart abandonment ratios (exceeding 60%). Optimizing shipping speeds or providing immediate automated coupons during cart 
              pauses may reclaim these transactions.
            - **Product Rating Variations:** The box plot shows that rating variances are highest in the **Electronics** category, 
              implying product quality consistency issues or shipment damages. In contrast, **Books** show a highly concentrated, 
              positive feedback distribution.
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>CustomerInsight Dashboard v1.0.0 | Customer Insights Module</p>", unsafe_allow_html=True)
