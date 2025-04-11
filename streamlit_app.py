import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium

# Enhanced Configuration
st.set_page_config(
    page_title="Child Maltreatment Insights",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Trauma-Informed Design
st.markdown("""
<style>
    /* Soft, Empathetic Color Palette */
    :root {
        --primary-color: #4A6D7C;
        --secondary-color: #8AB6D6;
        --accent-color: #E9967A;
        --background-color: #F4F4F4;
        --text-color: #333333;
    }
    
    /* Improved Typography */
    .stMarkdown, .stText {
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        color: var(--text-color);
    }
    
    /* Gentle Interaction States */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary-color);
        transform: scale(1.05);
    }
    
    /* Softer Chart Styling */
    .chart-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Accessible Focus States */
    *:focus {
        outline: 3px solid var(--accent-color);
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Cached Data Functions
@st.cache_data(show_spinner=False)
def get_state_data():
    data = {
        "State": ["Massachusetts", "Mississippi", "New Jersey", "California", "Texas",
                  "Florida", "New York", "Illinois", "Ohio", "Michigan"],
        "Victims": [20000, 15000, 18000, 80000, 75000,
                    65000, 70000, 50000, 40000, 35000],
        "Victim_Rate": [16.5, 12.0, 1.6, 8.0, 9.2,
                        10.1, 11.3, 7.5, 6.8, 5.5],
        "Fatalities": [300, 400, 150, 600, 500,
                       550, 500, 350, 300, 250],
        "Latitude": [42.4072, 32.3547, 40.0583, 36.7783, 31.9686,
                     27.6648, 43.2994, 40.6331, 40.4173, 44.3148],
        "Longitude": [-71.3824, -89.3985, -74.4057, -119.4179, -99.9018,
                      -81.5158, -74.2179, -89.3985, -82.9071, -85.6024]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_national_trends():
    data = {
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Victims": [678000, 660000, 650000, 640000, 558899],
        "Fatalities": [1700, 1750, 1800, 1850, 1990]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_disparities_data():
    data = {
        "Race": ["American Indian/Alaska Native", "African American", "White", "Hispanic", "Asian"],
        "Victim_Rate": [14.3, 12.1, 6.0, 6.5, 4.0],
        "Population_Percentage": [1.3, 13.4, 60.1, 18.5, 5.9]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_survivor_stories():
    return [
        {
            "quote": "Healing is not linear. Some days are harder than others, but I am more than what happened to me.",
            "name": "Anonymous Survivor",
            "theme": "Resilience"
        },
        {
            "quote": "Breaking the silence was my first step towards reclaiming my power.",
            "name": "Survivor Advocate",
            "theme": "Empowerment"
        }
    ]

# Content Warning Function
def display_content_warning():
    st.markdown("""
    ## 🕊️ Content Warning
    
    This dashboard contains sensitive information about child maltreatment. 
    If you feel uncomfortable or need support, please:
    
    - Reach out to a trusted person
    - Contact the National Child Abuse Hotline: **1-800-422-4453**
    - Take breaks as needed
    
    Your emotional safety is our priority.
    """)

# Main App Structure
def main():
    # Sidebar Navigation with Compassionate Design
    st.sidebar.title("🕊️ Child Maltreatment Insights")
    st.sidebar.markdown("*Empowering Understanding, Supporting Healing*")
    
    # Enhanced Navigation with Context
    page = st.sidebar.radio(
        "Explore Our Insights", 
        [
            "Home", 
            "National Overview", 
            "State Perspectives", 
            "Demographic Insights", 
            "Survivor Voices", 
            "Understanding Prevention", 
            "Support Resources"
        ],
        help="Navigate through different perspectives of our child protection data"
    )

    # Content Warning on Home Page
    if page == "Home":
        display_content_warning()
        
        st.title("Child Maltreatment: A Comprehensive Insight")
        
        # Empathetic Introduction
        st.markdown("""
        ## Understanding to Heal, Learning to Protect
        
        This dashboard is more than data—it's a commitment to understanding, 
        preventing, and supporting survivors of child maltreatment.
        
        Our mission is to:
        - Raise awareness
        - Provide compassionate insights
        - Support prevention efforts
        - Amplify survivor voices
        """)
        
        # Key Statistics Highlight
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Victims", "558,899", "Reported in 2022")
        with col2:
            st.metric("Child Fatalities", "1,990", "A tragic reality")
        with col3:
            st.metric("Prevention Goal", "100% Protection", "Our Collective Commitment")

    elif page == "National Overview":
        st.title("National Trends in Child Maltreatment")
        
        # Trends Visualization
        trends_df = get_national_trends()
        
        # Victims Trend
        st.markdown("### Reported Victims Over Time")
        victims_chart = alt.Chart(trends_df).mark_line(point=True, color='#4A6D7C').encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Victims:Q", title="Number of Victims"),
            tooltip=["Year", "Victims"]
        ).properties(
            width=700,
            height=400
        ).interactive()
        st.altair_chart(victims_chart, use_container_width=True)
        
        # Contextual Explanation
        st.info("""
        **Data Interpretation**: 
        While the number of reported victims has decreased, each number represents 
        a child's lived experience. Our goal is prevention and comprehensive support.
        """)

    # Similar compassionate, informative design for other pages...
    # (The rest of the pages would follow similar principles)

    # Footer with Support Resources
    st.markdown("---")
    st.markdown("""
    ### Need Support?
    - **National Child Abuse Hotline**: 1-800-422-4453
    - **Crisis Text Line**: Text HOME to 741741
    
    © 2025 Child Maltreatment Insights | Compassion in Data
    """)

# Run the app
if __name__ == "__main__":
    main()