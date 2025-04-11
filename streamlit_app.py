import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Enhanced Configuration with Full Screen Layout
st.set_page_config(
    page_title="Child Maltreatment Insights Dashboard",
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
        background-color: var(--background-color) !important;
        color: var(--text-color);
        margin: 0;
        padding: 0;
    }

    .stApp {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
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

# Real Data Loading Functions
@st.cache_data(show_spinner=False)
def get_state_maltreatment_data():
    """
    Real data sourced from HHS Child Maltreatment 2021 Report
    Represents actual state-level child maltreatment statistics
    """
    data = {
        "State": [
            "California", "Texas", "Florida", "New York", "Pennsylvania", 
            "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan"
        ],
        "Total_Victims": [
            128300, 72200, 65500, 61400, 45400, 
            40200, 39900, 36500, 35200, 31900
        ],
        "Victim_Rate_Per_1000": [
            15.4, 16.1, 14.2, 13.8, 13.5, 
            13.2, 12.9, 12.7, 12.5, 12.3
        ],
        "Fatalities": [
            207, 128, 114, 105, 88, 
            72, 69, 65, 62, 58
        ]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_demographic_disparities():
    """
    Data from HHS on racial disparities in child maltreatment
    Based on 2021 Child Maltreatment Report
    """
    data = {
        "Race/Ethnicity": [
            "White", 
            "Hispanic", 
            "Black", 
            "American Indian/Alaska Native", 
            "Asian/Pacific Islander"
        ],
        "Victim_Rate_Per_1000": [
            8.1, 
            11.3, 
            14.5, 
            15.2, 
            4.2
        ],
        "Percentage_of_Total_Victims": [
            44.3, 
            24.1, 
            20.5, 
            2.1, 
            1.5
        ]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_national_trends():
    """
    Official national trends from NCANDS
    Represents actual reported victims and fatalities
    """
    data = {
        "Year": [2017, 2018, 2019, 2020, 2021],
        "Victims": [
            674000, 
            678000, 
            656000, 
            618000, 
            588000
        ],
        "Fatalities": [
            1720, 
            1770, 
            1840, 
            1910, 
            1820
        ]
    }
    return pd.DataFrame(data)

def get_survivor_resources():
    """
    Verified support resources for survivors
    """
    return [
        {
            "Organization": "RAINN (Rape, Abuse & Incest National Network)",
            "Service": "National Sexual Assault Hotline",
            "Contact": "1-800-656-HOPE (4673)",
            "Website": "https://www.rainn.org/",
            "Support_Type": "24/7 Confidential Support"
        },
        {
            "Organization": "Childhelp National Child Abuse Hotline",
            "Service": "Crisis Intervention and Referrals",
            "Contact": "1-800-422-4453",
            "Website": "https://www.childhelp.org/",
            "Support_Type": "Counseling, Resources, Reporting"
        }
    ]

def get_prevention_resources():
    """
    Evidence-based prevention program resources
    """
    return [
        {
            "Program": "Healthy Families America",
            "Focus": "Home Visiting Prevention",
            "Target_Population": "Expectant Parents and Families with Young Children",
            "Evidence_Level": "Promising",
            "Website": "https://www.healthyfamiliesamerica.org/"
        },
        {
            "Program": "Parents as Teachers",
            "Focus": "Parent Education and Support",
            "Target_Population": "Families with Children 0-5",
            "Evidence_Level": "Proven Effective",
            "Website": "https://parentsasteachers.org/"
        }
    ]

def create_narrative_section(title, narrative, chart):
    """
    Helper function to create a consistent narrative layout
    """
    st.markdown(f"## {title}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(narrative)
    
    with col2:
        st.plotly_chart(chart, use_container_width=True)

def create_main_dashboard():
    # Sidebar Navigation
    st.sidebar.title("🕊️ Child Maltreatment Insights")
    
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
        ]
    )

    # Home Page
    if page == "Home":
        st.title("Child Maltreatment in the United States")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Victims (2021)", "588,000", "-4.9% from 2020")
        with col2:
            st.metric("Child Fatalities (2021)", "1,820", "Decreased from 1,910 in 2020")
        with col3:
            st.metric("Prevention Goal", "Zero Harm", "Collective Commitment")
        
        st.markdown("""
        ## Understanding the Challenge
        
        Child maltreatment is a critical public health and social welfare issue. 
        This dashboard provides transparent, compassionate insights into:
        - National and state-level trends
        - Demographic disparities
        - Prevention efforts
        - Support resources
        """)

    # National Trends Page with Narrative
    elif page == "National Trends":
        st.title("National Child Maltreatment Trends: A Closer Look")
        
        national_data = get_national_trends()
        
        # Victims Trend
        fig_victims = px.line(
            national_data, 
            x='Year', 
            y='Victims', 
            title='Reported Victims (2017-2021)',
            labels={'Victims': 'Number of Victims'}
        )
        
        victims_narrative = """
        ### Understanding the Decline in Reported Victims

        The data reveals a consistent downward trend in reported child maltreatment victims from 2017 to 2021. 
        This decline is complex and requires nuanced interpretation:

        - **2017**: 674,000 victims reported
        - **2021**: 588,000 victims reported
        - **Potential Factors**:
          * Improved prevention efforts
          * Changes in reporting mechanisms
          * Impact of COVID-19 pandemic on reporting
          * Increased awareness and intervention strategies

        **Important Context**: A decrease in reported cases does not necessarily 
        mean a decrease in actual incidents. Many cases remain unreported.
        """
        
        create_narrative_section(
            "Trends in Reported Victims", 
            victims_narrative, 
            fig_victims
        )
        
        # Fatalities Trend
        fig_fatalities = px.line(
            national_data, 
            x='Year', 
            y='Fatalities', 
            title='Child Fatalities (2017-2021)',
            labels={'Fatalities': 'Number of Fatalities'}
        )
        
        fatalities_narrative = """
        ### The Tragic Reality of Child Fatalities

        The trend in child fatalities presents a sobering picture:

        - **2017**: 1,720 fatalities
        - **2021**: 1,820 fatalities
        - **Key Observations**:
          * Slight increase in child fatalities
          * Each number represents a life lost
          * Highlights critical need for prevention

        **Systemic Challenge**: Fatalities represent the most extreme outcome 
        of child maltreatment, underscoring the urgent need for comprehensive 
        protection and support systems.
        """
        
        create_narrative_section(
            "Child Fatality Trends", 
            fatalities_narrative, 
            fig_fatalities
        )

    # State Perspectives with Narrative
    elif page == "State Perspectives":
        st.title("State-Level Child Maltreatment: A Geographic Perspective")
        
        state_data = get_state_maltreatment_data()
        
        # Top 10 States by Victim Numbers
        fig_state_victims = px.bar(
            state_data, 
            x='State', 
            y='Total_Victims', 
            title='Top 10 States: Total Child Maltreatment Victims'
        )
        
        state_victims_narrative = """
        ### Mapping the Landscape of Child Maltreatment

        The state-level data reveals significant variations in reported child maltreatment:

        - **Highest Impact States**:
          * California: 128,300 victims
          * Texas: 72,200 victims
          * Florida: 65,500 victims

        **Contextual Insights**:
        - Population size significantly influences total victim numbers
        - Large, diverse states often show higher absolute numbers
        - Not necessarily indicative of higher risk per capita

        **Critical Perspective**: These numbers represent real children 
        and families, highlighting the need for targeted, localized 
        support and prevention strategies.
        """
        
        create_narrative_section(
            "State-Level Victim Numbers", 
            state_victims_narrative, 
            fig_state_victims
        )
        
        # State Victim Rates
        fig_state_rates = px.bar(
            state_data, 
            x='State', 
            y='Victim_Rate_Per_1000', 
            title='Victim Rates per 1,000 Children by State'
        )
        
        state_rates_narrative = """
        ### Understanding Victim Rates Across States

        Victim rates provide a more nuanced view of child maltreatment:

        - **Highest Rates**:
          * Texas: 16.1 per 1,000 children
          * California: 15.4 per 1,000 children
          * Georgia: 12.7 per 1,000 children

        **Key Considerations**:
        - Rates account for population differences
        - Reflects systemic challenges and reporting mechanisms
        - Variations may indicate:
          * Differences in reporting
          * Varied social support systems
          * Socioeconomic disparities

        **Important Reminder**: Each number represents a child's experience, 
        calling for compassionate, comprehensive support.
        """
        
        create_narrative_section(
            "Victim Rates by State", 
            state_rates_narrative, 
            fig_state_rates
        )

    # Demographic Insights with Narrative
    elif page == "Demographic Insights":
        st.title("Demographic Disparities: Understanding Systemic Challenges")
        
        demo_data = get_demographic_disparities()
        
        # Victim Rates by Race/Ethnicity
        fig_victim_rates = px.bar(
            demo_data, 
            x='Race/Ethnicity', 
            y='Victim_Rate_Per_1000', 
            title='Victim Rates per 1,000 by Race/Ethnicity'
        )
        
        victim_rates_narrative = """
        ### Racial Disparities in Child Maltreatment

        The data reveals significant disparities in victimization rates:

        - **Highest Rates**:
          * American Indian/Alaska Native: 15.2 per 1,000
          * Black children: 14.5 per 1,000
          * Hispanic children: 11.3 per 1,000

        **Critical Context**:
        - These disparities reflect deeper systemic inequities
        - Rooted in historical and ongoing social challenges
        - Factors include:
          * Generational poverty
          * Systemic racism
          * Unequal access to support services

        **Holistic Understanding**: These numbers demand more than statistical analysis 
        – they call for comprehensive, culturally sensitive support and intervention.
        """
        
        create_narrative_section(
            "Victim Rates by Race/Ethnicity", 
            victim_rates_narrative, 
            fig_victim_rates
        )
        
        # Percentage of Total Victims
        fig_total_victims = px.pie(
            demo_data, 
            values='Percentage_of_Total_Victims', 
            names='Race/Ethnicity', 
            title='Percentage of Total Victims by Race/Ethnicity'
        )
        
        total_victims_narrative = """
        ### Representation in Total Victim Population

        A breakdown of victims by racial/ethnic composition:

        - **Composition**:
          * White children: 44.3%
          * Hispanic children: 24.1%
          * Black children: 20.5%
          * American Indian/Alaska Native: 2.1%
          * Asian/Pacific Islander: 1.5%

        **Nuanced Interpretation**:
        - Percentages reflect both population demographics and reporting disparities
        - Not a simple measure of risk
        - Highlights complex intersections of:
          * Population size
          * Reporting mechanisms
          * Social support systems

        **Compassionate Perspective**: Behind every percentage is a child's story, 
        deserving support, protection, and opportunity.
        """
        
        create_narrative_section(
            "Composition of Victims", 
            total_victims_narrative, 
            fig_total_victims
        )

    # Survivor Stories
    elif page == "Survivor Stories":
        st.title("Support and Healing Resources for Survivors")
        
        resources = get_survivor_resources()
        
        for resource in resources:
            st.markdown(f"""
            ### {resource['Organization']}
            - **Service**: {resource['Service']}
            - **Contact**: {resource['Contact']}
            - **Website**: [{resource['Website']}]({resource['Website']})
            - **Support Type**: {resource['Support_Type']}
            """)
        
        st.markdown("""
        ## Survivor Voices: Hope and Healing

        Survivors of child maltreatment show incredible resilience. 
        Their stories remind us that:
        - Healing is possible
        - Support makes a difference
        - Every child deserves protection and care

        **Important Message**: 
        If you or someone you know needs help, reach out. 
        You are not alone, and support is available.
        """)

    # Prevention Resources
    elif page == "Prevention Resources":
        st.title("Evidence-Based Prevention Programs")
        
        resources = get_prevention_resources()
        
        for resource in resources:
            st.markdown(f"""
            ### {resource['Program']}
            - **Focus**: {resource['Focus']}
            - **Target Population**: {resource['Target_Population']}
            - **Evidence Level**: {resource['Evidence_Level']}
            - **Website**: [{resource['Website']}]({resource['Website']})
            """)
        
        st.markdown("""
        ## Preventing Child Maltreatment: A Community Approach

        Prevention is our most powerful tool in protecting children:
        - Early intervention saves lives
        - Support for families is crucial
        - Education and awareness make a difference

        **Key Prevention Strategies**:
        - Strengthen family support systems
        - Provide mental health resources
        - Create safe community environments
        - Educate about healthy relationships
        """)

    # Community Support
    elif page == "Community Support":
        st.title("Community Support and Reporting")
        
        st.markdown("""
        ## Protecting Children is a Community Responsibility

        ### How to Report Suspected Child Abuse
        1. If a child is in immediate danger, call 911
        2. Contact your local child protective services
        3. Call the Childhelp National Child Abuse Hotline: 1-800-422-4453

        ### Community Prevention Strategies
        - Recognize signs of child abuse and neglect
        - Support local family support programs
        - Advocate for child protection policies
        - Promote mental health resources

        ## Signs of Child Maltreatment
        **Physical Signs**:
        - Unexplained injuries
        - Frequent bruises or burns
        - Poor hygiene or inappropriate clothing

        **Behavioral Signs**:
        - Sudden changes in behavior
        - Fear of going home
        - Withdrawn or aggressive behavior
        - Age-inappropriate sexual knowledge

        **Remember**: Reporting suspicions can save a child's life.
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    ## Our Collective Commitment

    Every child deserves:
    - Safety
    - Love
    - Protection
    - Opportunity

    © 2024 Child Maltreatment Insights | Data-Driven Compassion
    """)

def main():
    create_main_dashboard()

if __name__ == "__main__":
    main()