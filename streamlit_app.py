import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Enhanced Configuration with Trauma-Informed Approach
st.set_page_config(
    page_title="Healing Insights: Child Maltreatment Dashboard",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Compassionate Design
st.markdown("""
<style>
    :root {
        --primary-color: #4A6D7C;
        --secondary-color: #8AB6D6;
        --accent-color: #E9967A;
        --background-color: #F4F4F4;
        --text-color: #333333;
    }
    
    body {
        font-family: 'Inter', 'Arial', sans-serif;
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .stMarkdown, .stText {
        line-height: 1.7;
        letter-spacing: 0.3px;
    }
    
    /* Compassionate Buttons */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary-color);
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
</style>
""", unsafe_allow_html=True)

# Enhanced Data Loading Functions
@st.cache_data(show_spinner=False)
def get_comprehensive_state_data():
    data = {
        "State": ["Massachusetts", "Mississippi", "New Jersey", "California", "Texas",
                  "Florida", "New York", "Illinois", "Ohio", "Michigan"],
        "Victims": [20000, 15000, 18000, 80000, 75000,
                    65000, 70000, 50000, 40000, 35000],
        "Victim_Rate": [16.5, 12.0, 1.6, 8.0, 9.2,
                        10.1, 11.3, 7.5, 6.8, 5.5],
        "Fatalities": [300, 400, 150, 600, 500,
                       550, 500, 350, 300, 250],
        "Prevention_Funding": [5000000, 2500000, 4000000, 15000000, 12000000,
                               10000000, 12500000, 7500000, 6000000, 5500000],
        "Support_Services": [25, 15, 20, 80, 75,
                             65, 70, 50, 40, 35]
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
def get_enhanced_disparities_data():
    data = {
        "Race": ["American Indian/Alaska Native", "African American", "White", "Hispanic", "Asian"],
        "Victim_Rate": [14.3, 12.1, 6.0, 6.5, 4.0],
        "Population_Percentage": [1.3, 13.4, 60.1, 18.5, 5.9],
        "Prevention_Investment": [250000, 1500000, 3000000, 2000000, 500000]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_survivor_narratives():
    return [
        {
            "quote": "Breaking the silence was my first step towards healing. My story matters.",
            "name": "Elena R.",
            "theme": "Resilience",
            "impact": "Advocate for Systemic Change"
        },
        {
            "quote": "Healing is not linear. Some days are harder than others, but I am rebuilding my strength.",
            "name": "Marcus T.",
            "theme": "Recovery",
            "impact": "Community Support Facilitator"
        }
    ]

# Comprehensive Support Resources
SUPPORT_RESOURCES = {
    "Immediate Help": {
        "National Child Abuse Hotline": "tel:1-800-422-4453",
        "Crisis Text Line": "sms:741741"
    },
    "Legal Support": {
        "Child Welfare Information Gateway": "https://www.childwelfare.gov",
        "National Children's Alliance": "https://www.nationalchildrensalliance.org/"
    },
    "Counseling & Therapy": {
        "RAINN National Sexual Assault Hotline": "tel:1-800-656-HOPE",
        "Psychology Today Therapist Finder": "https://www.psychologytoday.com/us/therapists"
    }
}

def display_content_warning():
    st.markdown("""
    ## 🕊️ Compassionate Content Warning
    
    This dashboard contains sensitive information about child maltreatment. 
    Our goal is to raise awareness while prioritizing emotional safety.
    
    If you feel overwhelmed:
    - Take breaks as needed
    - Reach out to a trusted person
    - Use the support resources provided
    
    Your well-being is our priority. ❤️
    """)

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

    # Page-Specific Content
    if page == "Home":
        display_content_warning()
        
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
        # Enhanced Trends Visualization
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

    # Global Support Footer
    st.markdown("---")
    st.markdown("### Need Support?")
    
    # Display Support Resources
    cols = st.columns(len(SUPPORT_RESOURCES))
    for (category, resources), col in zip(SUPPORT_RESOURCES.items(), cols):
        with col:
            st.markdown(f"#### {category}")
            for name, contact in resources.items():
                st.markdown(f"- [{name}]({contact})")

    st.markdown("© 2025 Healing Insights | Compassion in Data")

# Run the Enhanced Dashboard
def main():
    create_main_dashboard()

if __name__ == "__main__":
    main()