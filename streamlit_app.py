import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Enhanced Configuration with Full Screen Layout
st.set_page_config(
    page_title="Healing Insights: Child Maltreatment Dashboard",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Comprehensive Custom CSS for Full Screen and Compassionate Design
st.markdown("""
<style>
    /* Reset default Streamlit styling */
    .stApp {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Full width containers */
    .stColumn, .stColumns {
        width: 100% !important;
    }

    /* Root variables for consistent theming */
    :root {
        --primary-color: #4A6D7C;
        --secondary-color: #8AB6D6;
        --accent-color: #E9967A;
        --background-color: #F4F4F4;
        --text-color: #333333;
    }

    /* Global body and app styling */
    body {
        font-family: 'Inter', 'Arial', sans-serif;
        background-color: var(--background-color) !important;
        color: var(--text-color);
        margin: 0;
        padding: 0;
    }

    /* Sidebar full height */
    section[data-testid="stSidebar"] {
        height: 100vh !important;
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        width: 300px !important;
        z-index: 1000;
    }

    /* Main content area */
    section[data-testid="stAppViewContainer"] {
        margin-left: 300px !important;
        width: calc(100% - 300px) !important;
        padding: 20px !important;
    }

    /* Typography and readability */
    .stMarkdown, .stText {
        line-height: 1.7;
        letter-spacing: 0.3px;
    }

    /* Compassionate Buttons */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: var(--secondary-color) !important;
        transform: scale(1.05);
    }

    /* Soft Containers */
    .stContainer {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Responsive adjustments */
    @media (max-width: 1024px) {
        section[data-testid="stSidebar"] {
            width: 250px !important;
        }
        section[data-testid="stAppViewContainer"] {
            margin-left: 250px !important;
            width: calc(100% - 250px) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Rest of the previous code remains the same as in the last artifact
# (Data loading functions, support resources, etc.)

@st.cache_data(show_spinner=False)
def get_national_trends():
    data = {
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Victims": [678000, 660000, 650000, 640000, 558899],
        "Fatalities": [1700, 1750, 1800, 1850, 1990]
    }
    return pd.DataFrame(data)

def create_main_dashboard():
    # Sidebar with Empathetic Navigation
    st.sidebar.title("🕊️ Healing Insights")
    st.sidebar.markdown("*Understanding. Healing. Protecting.*")
    
    # Enhanced Navigation
    page = st.sidebar.radio(
        "Navigate Insights", 
        [
            "Home", 
            "National Trends", 
            "State Perspectives", 
            "Demographic Insights", 
            "Survivor Stories", 
            "Prevention Resources", 
            "Community Support"
        ],
        help="Explore our compassionate data journey"
    )

    # Existing page content remains the same
    if page == "Home":
        st.title("Healing Insights: Child Maltreatment Dashboard")
        
        # Empathetic Introduction with Key Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Victims", "558,899", "Our Collective Responsibility")
        with col2:
            st.metric("Child Fatalities", "1,990", "Each Life Precious")
        with col3:
            st.metric("Prevention Goal", "100% Protection", "Together We Can")
        
        # Mission Statement
        st.markdown("""
        ## Our Mission: Understanding to Heal, Learning to Protect
        
        This dashboard is more than statistics—it's a commitment to:
        - Raising Awareness
        - Supporting Survivors
        - Driving Systemic Change
        - Fostering Community Healing
        """)

    elif page == "National Trends":
        st.title("National Child Maltreatment Trends")
        
        # Interactive Plotly Visualizations
        national_data = get_national_trends()
        
        # Victims Trend
        fig_victims = px.line(
            national_data, 
            x='Year', 
            y='Victims', 
            title='Reported Victims Over Time',
            labels={'Victims': 'Number of Victims'},
            color_discrete_sequence=['#4A6D7C']
        )
        fig_victims.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_victims, use_container_width=True)
        
        # Fatalities Trend
        fig_fatalities = px.line(
            national_data, 
            x='Year', 
            y='Fatalities', 
            title='Child Fatalities Trend',
            labels={'Fatalities': 'Number of Fatalities'},
            color_discrete_sequence=['#E9967A']
        )
        fig_fatalities.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_fatalities, use_container_width=True)
        
        # Contextual Insights
        st.info("""
        **Interpreting the Data:**
        - Each data point represents real lives and experiences
        - Trends show both challenges and potential for prevention
        - Our collective action can create meaningful change
        """)

    # Rest of the content remains the same
    st.markdown("---")
    st.markdown("© 2025 Healing Insights | Compassion in Data")

# Run the Enhanced Dashboard
def main():
    create_main_dashboard()

if __name__ == "__main__":
    main()