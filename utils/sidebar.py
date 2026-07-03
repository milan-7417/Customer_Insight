import os
import streamlit as st
import pandas as pd

def load_sidebar(df, page_name=""):
    """Loads the unified sidebar with logo, navigation, page-specific filters,
    and injects the custom stylesheet. Returns the filtered dataframe.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    css_path = os.path.join(project_root, "assets", "style.css")
    logo_path = os.path.join(project_root, "assets", "logo.png")
    
    # Inject Custom CSS
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # Sidebar Logo and Title
    with st.sidebar:
        # Display logo if it exists
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
            
        st.markdown("<h2 style='text-align: center; color: #7C3AED; margin-top:-10px;'>CustomerInsight</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.85rem; color: #64748B;'>Enterprise Customer Analytics & Business Intelligence Dashboard</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Quick-Links
        st.subheader("Navigation")
        st.page_link("app.py", label="Home / Overview", icon="🏠")
        st.page_link("pages/1_Executive_Dashboard.py", label="Executive Dashboard", icon="📊")
        st.page_link("pages/2_Customer_Demographics.py", label="Demographics", icon="👥")
        st.page_link("pages/3_Purchase_Behavior.py", label="Purchase Behavior", icon="🛒")
        st.page_link("pages/4_Spending_Analysis.py", label="Spending Analysis", icon="💰")
        st.page_link("pages/5_Customer_Insights.py", label="Customer Insights", icon="🧠")
        st.page_link("pages/6_Business_Insights.py", label="Business Insights", icon="📈")
        
        st.markdown("---")
        
        # Global Filters Section
        st.subheader("Global Filters")
        
        # 1. State Filter
        states = sorted(list(df['State'].unique()))
        selected_states = st.multiselect(
            "Select States",
            options=states,
            placeholder="All States"
        )
        
        # 2. Membership Filter
        memberships = sorted([str(m) for m in df['Membership_Type'].unique() if pd.notna(m)])
        selected_memberships = st.multiselect(
            "Membership Type",
            options=memberships,
            placeholder="All Tiers"
        )
        
        # 3. Gender Filter
        genders = sorted(list(df['Gender'].unique()))
        selected_genders = st.multiselect(
            "Gender",
            options=genders,
            placeholder="All Genders"
        )
        
        # 4. Age Slider
        min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
        selected_age_range = st.slider(
            "Age Range",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
        )
        
        # 5. Product Category Filter
        categories = sorted(list(df['Preferred_Category'].unique()))
        selected_categories = st.multiselect(
            "Preferred Category",
            options=categories,
            placeholder="All Categories"
        )
        
        st.markdown("---")
        # System Meta
        st.markdown("<p style='text-align: center; font-size: 0.75rem; color: #94A3B8;'>Version 1.0.0<br>© 2026 CustomerInsight</p>", unsafe_allow_html=True)
        
    # Apply Filtering Logic to Dataframe
    filtered_df = df.copy()
    
    if selected_states:
        filtered_df = filtered_df[filtered_df['State'].isin(selected_states)]
        
    if selected_memberships:
        filtered_df = filtered_df[filtered_df['Membership_Type'].isin(selected_memberships)]
        
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
        
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Preferred_Category'].isin(selected_categories)]
        
    # Filter Age Range
    filtered_df = filtered_df[(filtered_df['Age'] >= selected_age_range[0]) & (filtered_df['Age'] <= selected_age_range[1])]
    
    return filtered_df
