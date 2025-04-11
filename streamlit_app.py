import streamlit as st
import time
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import numpy as np
import textwrap
from PIL import Image
from io import BytesIO
import base64

# This must be the first Streamlit command!
st.set_page_config(
    page_title="Child Maltreatment Data Story",
    page_icon="👧👦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Custom CSS for better design
# ------------------------------
st.markdown("""
<style>
    /* Color scheme */
    :root {
        --primary: #6A8EAE;  /* Calming blue */
        --secondary: #F9E9D9;  /* Soft cream */
        --accent: #FF9E7A;  /* Gentle coral for emphasis */
        --text: #4A4A4A;  /* Soft black for readability */
        --light-bg: #F7F7F7;  /* Light background */
    }
    
    /* Base styling */
    body {
        color: var(--text);
        background-color: var(--light-bg);
    }
    
    h1, h2, h3 {
        color: var(--primary);
        font-weight: 600;
    }
    
    /* Cards for statistics */
    .stat-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-left: 5px solid var(--primary);
    }
    
    /* Quote styling */
    .quote-container {
        background-color: var(--secondary);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .quote-container:before {
        content: """;
        font-size: 4rem;
        color: var(--accent);
        position: absolute;
        top: -15px;
        left: 10px;
        opacity: 0.3;
    }
    
    /* Key takeaway styling */
    .takeaway {
        background-color: #F3F8FF;
        border-left: 4px solid var(--primary);
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Narrative section styling */
    .narrative-section {
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #5A7A96;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--accent);
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted var(--accent);
    }
    
    /* Age breakdown view */
    .age-segment {
        width: 100%;
        height: 30px;
        display: flex;
        margin-bottom: 5px;
    }
    
    /* Resource cards */
    .resource-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 0.5rem;
    }
    
    /* Header for pages */
    .page-header {
        margin-bottom: 2rem;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 1rem;
    }
    
    /* Impact meter */
    .impact-meter {
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .impact-meter-fill {
        height: 100%;
        background-color: var(--accent);
        border-radius: 5px;
    }
    
    /* Create centered layout for charts */
    .chart-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    /* Make sure Streamlit components are also styled */
    div.stRadio > div {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 4px 4px 0 0;
        border: none;
        padding: 0.5rem 1rem;
        color: var(--text);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Helper Functions
# ------------------------------

def create_stat_card(title, value, subtext, icon="📊"):
    """Create a visually appealing stat card with icon"""
    html = f"""
    <div class="stat-card">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 1rem;">{icon}</div>
            <div>
                <h3 style="margin-bottom: 0.5rem;">{title}</h3>
                <div style="font-size: 1.8rem; font-weight: bold; color: #6A8EAE;">{value}</div>
                <div style="font-size: 0.9rem; color: #666;">{subtext}</div>
            </div>
        </div>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

def display_quote(quote, author):
    """Display a quote in a styled container"""
    html = f"""
    <div class="quote-container">
        <p style="font-style: italic; font-size: 1.1rem;">{quote}</p>
        <p style="text-align: right; font-weight: bold;">— {author}</p>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

def display_key_takeaway(text):
    """Display a key takeaway/insight from the data"""
    html = f"""
    <div class="takeaway">
        <strong>Key Insight:</strong> {text}
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

def progress_animation():
    """Create an animated progress indicator"""
    progress_bar = st.progress(0)
    for percent in range(0, 101, 5):
        progress_bar.progress(percent)
        time.sleep(0.05)  # Faster animation
    return progress_bar

def create_age_breakdown_viz(data_dict):
    """Create a visual breakdown of victim ages"""
    total = sum(data_dict.values())
    html = "<div style='width:100%;'>"
    colors = ["#6A8EAE", "#7FB5B5", "#9ECCAB", "#C1E3A6", "#F9E9D9", "#FFD1B8", "#FF9E7A"]
    
    for i, (age, count) in enumerate(data_dict.items()):
        percentage = (count / total) * 100
        html += f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex; align-items:center; margin-bottom:0.3rem;">
                <div style="width:120px; font-size:0.9rem;">{age}</div>
                <div style="flex-grow:1; background-color:#f0f0f0; height:25px; border-radius:4px;">
                    <div style="width:{percentage}%; height:100%; background-color:{colors[i%len(colors)]}; border-radius:4px; display:flex; align-items:center; justify-content:center; color:white; font-size:0.8rem;">
                        {percentage:.1f}%
                    </div>
                </div>
            </div>
            <div style="font-size:0.8rem; color:#666; margin-left:120px;">
                {count:,} children
            </div>
        </div>
        """
    
    html += "</div>"
    return st.markdown(html, unsafe_allow_html=True)

def create_impact_meter(value, max_value, label):
    """Create a visual impact meter"""
    percentage = min(100, (value / max_value) * 100)
    html = f"""
    <div>
        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <div style="font-size:0.9rem;">{label}</div>
            <div style="font-size:0.9rem; font-weight:bold;">{value:,}</div>
        </div>
        <div class="impact-meter">
            <div class="impact-meter-fill" style="width:{percentage}%;"></div>
        </div>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

def fade_in_text(text, key):
    """Create a fade-in effect for text"""
    # Simplified version without JavaScript
    st.markdown(f"<div id='fade-{key}' style='opacity:1; transition: opacity 2s;'>{text}</div>", unsafe_allow_html=True)

# ------------------------------
# Data Loading Functions
# ------------------------------

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
        "Victim_Rate": [14.3, 12.1, 6.0, 6.5, 4.0]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_quotes():
    # List of dictionaries containing survivor quotes
    return [
        {
            "quote": "I would write letters to my third-grade teacher. I never had the courage to send them, but I always held out hope that someday she would notice. I just wished so often that she would save me.",
            "name": "Tiffani Shurtleff"
        },
        {
            "quote": "My childhood was filled with physical abuse from the person who was supposed to love me; sexual abuse from people who were supposed to protect me… I just wanted someone to save me. I needed help. I needed to be rescued.",
            "name": "Kristina"
        },
        {
            "quote": "I didn't know it wasn't normal. I thought every kid lived in fear. I wish someone had asked the right questions or noticed the signs.",
            "name": "Michael"
        },
        {
            "quote": "When my teacher finally reported what was happening, it was like someone turned on a light in a very dark room. For the first time, I understood I deserved better.",
            "name": "Sophia"
        }
    ]

@st.cache_data(show_spinner=False)
def get_prevention_success_stories():
    return [
        {
            "title": "Family Resource Centers",
            "impact": "30% reduction in reported cases in participating communities",
            "description": "Centers providing parenting classes, economic support and counseling have shown significant impacts in reducing maltreatment cases."
        },
        {
            "title": "Home Visiting Programs",
            "impact": "50% fewer emergency room visits for participating families",
            "description": "Programs that connect new parents with health providers and parenting experts show dramatic improvements in child health outcomes."
        },
        {
            "title": "Trauma-Informed Schools",
            "impact": "85% increase in identification of at-risk children",
            "description": "When educators are trained to recognize signs of maltreatment and respond appropriately, intervention happens earlier."
        }
    ]

@st.cache_data(show_spinner=False)
def get_age_breakdown():
    # Age breakdown of victims
    return {
        "Under 1 year": 45800,
        "1-3 years": 112000, 
        "4-7 years": 120000,
        "8-11 years": 105000,
        "12-15 years": 95000,
        "16-17 years": 81099
    }

@st.cache_data(show_spinner=False)
def get_maltreatment_types():
    # Types of maltreatment with percentages
    return {
        "Neglect": 74.2,
        "Physical Abuse": 16.8,
        "Sexual Abuse": 8.5,
        "Psychological Abuse": 5.6,
        "Other": 2.1
    }

@st.cache_data(show_spinner=False)
def get_intervention_data():
    # Data for intervention outcomes
    return {
        "Type": ["Early Intervention", "Crisis Response", "No Intervention"],
        "Positive Outcomes": [78, 45, 10],
        "Children Retraumatized": [5, 25, 65],
        "Families Preserved": [85, 40, 15]
    }

# ------------------------------
# Page Layout & Navigation
# ------------------------------
with st.sidebar:
    st.image("https://static.vecteezy.com/system/resources/previews/016/742/386/original/child-protection-icon-free-vector.jpg", width=100)
    st.title("Navigation")
    
    # Create more intuitive navigation
    page = st.radio(
        "Select a section",
        [
            "📚 Introduction",
            "📖 The Full Story", 
            "📊 Data Explorer",
            "🗺️ Geographic Insights",
            "🔍 Understanding Disparities",
            "👥 Survivor Voices",
            "💡 Quiz & Learning",
            "🤝 Take Action"
        ]
    )
    
    # Quick facts always accessible in sidebar
    with st.expander("📌 Quick Facts", expanded=False):
        st.markdown("""
        - **Most victims** are under 3 years old
        - **Neglect** is the most common form (74%)
        - **Indigenous children** face the highest rates
        - **Prevention programs** show 30-50% effectiveness
        """)
    
    # User persona selection
    st.markdown("### I am a...")
    persona = st.selectbox(
        "Select your perspective",
        ["General Public", "Researcher/Academic", "Educator", "Healthcare Provider", "Social Worker", "Student"]
    )
    
    # Adjust content complexity based on persona
    complexity = {
        "General Public": "basic",
        "Researcher/Academic": "advanced",
        "Educator": "moderate",
        "Healthcare Provider": "moderate",
        "Social Worker": "advanced",
        "Student": "basic"
    }
    
    # Accessibility options
    with st.expander("⚙️ Accessibility Options"):
        text_size = st.select_slider(
            "Text Size",
            options=["Small", "Medium", "Large"],
            value="Medium"
        )
        
        # Apply text size changes
        if text_size == "Small":
            st.markdown("""
            <style>
                p, li, div {font-size: 0.9rem !important;}
                h1 {font-size: 1.8rem !important;}
                h2 {font-size: 1.5rem !important;}
                h3 {font-size: 1.2rem !important;}
            </style>
            """, unsafe_allow_html=True)
        elif text_size == "Large":
            st.markdown("""
            <style>
                p, li, div {font-size: 1.1rem !important;}
                h1 {font-size: 2.2rem !important;}
                h2 {font-size: 1.8rem !important;}
                h3 {font-size: 1.5rem !important;}
            </style>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 Child Maltreatment Data Story")

# ------------------------------
# Introduction Page
# ------------------------------
if page == "📚 Introduction":
    st.markdown('<div class="page-header">', unsafe_allow_html=True)
    st.title("Child Maltreatment Data Story")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Two-column layout for intro
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="narrative-section">
            <p>Every number in this dashboard represents a child's life and experience. Beyond the statistics are stories 
            of vulnerability, resilience, and the potential for change.</p>
            
            <p>This interactive experience invites you to explore the data on child maltreatment in the United States, 
            while keeping the human impact at the center of our understanding.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key statistics in attractive cards
        st.markdown("### At a Glance")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            create_stat_card("Annual Victims", "558,899", "Children in 2022", icon="👧👦")
        
        with col_b:
            create_stat_card("Child Fatalities", "1,990", "Lives lost in 2022", icon="💔")
            
        with col_c:
            create_stat_card("Highest Risk Age", "< 1 year", "25.3 per 1,000 infants", icon="👶")
    
    with col2:
        # Impact visualization - stylized illustration rather than photos 
        st.image("https://www.unicef.org/canada/sites/unicef.org.canada/files/styles/hero_desktop/public/UN0342728.jpg", use_container_width=True)
        st.caption("Every child deserves safety, care, and protection.")
    
    # Contextual introduction to the dashboard
    st.markdown("---")
    st.markdown("### How to Use This Data Story")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Start with the narrative:**
        - The "Full Story" provides context and meaning
        - Each section builds understanding progressively
        - Quotes from survivors humanize the statistics
        """)
        
        st.markdown("""
        **Explore the data:**
        - Compare trends across years and states
        - Understand demographic differences
        - See how interventions impact outcomes
        """)
    
    with col2:
        st.markdown("""
        **Take action:**
        - Learn about prevention approaches that work
        - Find resources for further learning
        - Discover ways to contribute to solutions
        """)
        
        # Call to action button
        if st.button("Begin the Journey", key="start_journey"):
            st.session_state.page = "📖 The Full Story"
            st.experimental_rerun()
    
    # Start with a survivor quote to humanize the data
    st.markdown("---")
    quote = get_quotes()[0]
    display_quote(quote["quote"], quote["name"])

# ------------------------------
# The Full Story Page (Narrative)
# ------------------------------
elif page == "📖 The Full Story":
    st.markdown('<div class="page-header">', unsafe_allow_html=True)
    st.title("The Story Behind the Numbers")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Progress tracker (visual breadcrumb)
    progress_steps = ["Introduction", "Understanding the Data", "Impact", "Hope & Action"]
    current_step = st.select_slider("Your journey", options=progress_steps, value="Introduction")
    
    # Dynamic content based on progress step
    if current_step == "Introduction":
        st.markdown("""
        <div class="narrative-section">
            <p>Child maltreatment affects hundreds of thousands of children each year in the United States.
            This is not just a collection of statistics, but a reality that impacts communities, families, and most 
            importantly, children themselves.</p>
            
            <p>The numbers we'll explore represent real experiences of vulnerability, harm, and in too many cases, 
            lives cut tragically short. But they also point toward opportunities for intervention, prevention, and healing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualization of current data
        st.markdown("### The Current Picture (2022)")
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a donut chart for maltreatment types
            maltreatment_data = get_maltreatment_types()
            fig = go.Figure(go.Pie(
                labels=list(maltreatment_data.keys()),
                values=list(maltreatment_data.values()),
                hole=.4,
                marker_colors=['#6A8EAE', '#7FB5B5', '#FF9E7A', '#C1E3A6', '#F9E9D9'],
                textinfo='label+percent'
            ))
            fig.update_layout(
                title="Types of Maltreatment",
                height=400,
                margin=dict(t=30, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Key insight
            display_key_takeaway("Neglect is by far the most common form of maltreatment, often stemming from poverty, substance abuse, and lack of support systems for families.")
            
        with col2:
            # Age breakdown with visual representation
            st.markdown("### Age Breakdown of Victims")
            create_age_breakdown_viz(get_age_breakdown())
            
            # Key insight
            display_key_takeaway("Infants and very young children are the most vulnerable, with risk decreasing as children age and develop more independence and communication abilities.")
    
    elif current_step == "Understanding the Data":
        st.markdown("""
        <div class="narrative-section">
            <p>Looking at the trends over the past five years reveals both progress and ongoing challenges. While overall case 
            numbers appear to be declining, fatality rates continue to rise—suggesting that the most severe cases 
            remain difficult to prevent.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualize trends with annotations
        trends_df = get_national_trends()
        
        # Create more visually engaging charts with annotations
        fig = px.line(trends_df, x="Year", y="Victims", markers=True, line_shape="spline",
                     color_discrete_sequence=["#6A8EAE"])
        
        # Add annotations for key points
        fig.add_annotation(
            x=2020, y=650000,
            text="COVID-19 pandemic begins",
            showarrow=True,
            arrowhead=1,
            ax=50, ay=-40
        )
        
        fig.add_annotation(
            x=2022, y=558899,
            text="17.6% decrease since 2018",
            showarrow=True,
            arrowhead=1,
            ax=-60, ay=40
        )
        
        fig.update_layout(
            title="Trend in Reported Victims (2018-2022)",
            height=400,
            margin=dict(t=40, b=0, l=0, r=0),
            yaxis_title="Number of Victims",
            xaxis_title="Year",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Fatality trend
        fig2 = px.line(trends_df, x="Year", y="Fatalities", markers=True, line_shape="spline",
                      color_discrete_sequence=["#FF9E7A"])
        
        fig2.add_annotation(
            x=2022, y=1990,
            text="17% increase since 2018",
            showarrow=True,
            arrowhead=1,
            ax=-50, ay=-40
        )
        
        fig2.update_layout(
            title="Trend in Child Fatalities (2018-2022)",
            height=400,
            margin=dict(t=40, b=0, l=0, r=0),
            yaxis_title="Number of Fatalities",
            xaxis_title="Year",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Key insight
        display_key_takeaway("The diverging trends between overall cases and fatalities suggest that while awareness and reporting may be improving overall, the most severe cases remain challenging to identify and prevent in time.")
        
        # Interactive element - year selection
        selected_year = st.slider("Select a Year to Explore", 2018, 2022, 2022)
        year_data = trends_df[trends_df["Year"] == selected_year].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            create_stat_card(f"Victims in {selected_year}", f"{year_data['Victims']:,}", "Reported cases", "👧👦")
        with col2:
            create_stat_card(f"Fatalities in {selected_year}", f"{year_data['Fatalities']:,}", "Lives lost", "💔")
    
    elif current_step == "Impact":
        st.markdown("""
        <div class="narrative-section">
            <p>Behind every statistic in this data is a child whose life has been altered. The impact of maltreatment 
            extends far beyond the immediate harm, creating long-term effects on development, health, and wellbeing.</p>
            
            <p>Research shows that childhood trauma can affect brain development, mental health, physical health, 
            educational outcomes, and future relationships. But early intervention can significantly mitigate these effects.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Impact visualization
        st.markdown("### Long-term Impact of Maltreatment")
        
        # Create a radar chart for impact areas
        impact_categories = ['Cognitive Development', 'Mental Health', 'Physical Health', 
                           'Educational Achievement', 'Relationship Skills', 'Economic Stability']
        
        # Values represent "reduced outcomes" compared to non-maltreated peers (higher = worse outcome)
        no_intervention = [65, 70, 60, 75, 80, 70]
        early_intervention = [25, 30, 20, 35, 40, 30]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=no_intervention,
            theta=impact_categories,
            fill='toself',
            name='Without Intervention',
            line_color='#FF9E7A',
            fillcolor='rgba(255, 158, 122, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=early_intervention,
            theta=impact_categories,
            fill='toself',
            name='With Early Intervention',
            line_color='#6A8EAE',
            fillcolor='rgba(106, 142, 174, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=500,
            margin=dict(t=40, b=40, l=80, r=80)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insight
        display_key_takeaway("Early intervention dramatically reduces the long-term negative impacts of maltreatment across all areas of development and functioning. The earlier the intervention, the better the outcomes.")
        
        # Add survivor voice
        display_quote(get_quotes()[3]["quote"], get_quotes()[3]["name"])
        
    elif current_step == "Hope & Action":
        st.markdown("""
        <div class="narrative-section">
            <p>Despite the sobering statistics, there is significant hope. Evidence-based prevention programs and early 
            interventions have demonstrated remarkable success in reducing maltreatment and improving outcomes for 
            affected children.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Success stories cards
        st.markdown("### What Works: Prevention Success Stories")
        
        success_stories = get_prevention_success_stories()
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, story in enumerate(success_stories):
            with cols[i]:
                st.markdown(f"""
                <div style="background-color: white; padding: 1.5rem; border-radius: 10px; height: 100%; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #6A8EAE;">
                    <h3>{story['title']}</h3>
                    <div style="font-size: 1.2rem; font-weight: bold; color: #FF9E7A; margin: 0.5rem 0;">
                        {story['impact']}
                    </div>
                    <p>{story['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Cost-benefit visualization
        st.markdown("### The Economic Case for Prevention")
        
        # Create bar chart for cost-benefit analysis
        programs = ["Home Visiting", "Parent Training", "Family Support", "No Prevention"]
        costs = [10000, 5000, 7500, 0]  # Cost per family
        savings = [65000, 35000, 40000, 0]  # Long-term societal savings
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=programs,
            y=costs,
            name='Program Cost per Family',
            marker_color='#6A8EAE'
        ))
        
        fig.add_trace(go.Bar(
            x=programs,
            y=savings,
            name='Long-term Societal Savings',
            marker_color='#FF9E7A'
        ))
        
        fig.update_layout(
            barmode='group',
            title="Cost vs. Benefit of Prevention Programs",
            xaxis_title="Prevention Approach",
            yaxis_title="Dollars",
            legend_title="Financial Impact",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insight
        display_key_takeaway("Prevention programs show a significant return on investment—every $1 invested in prevention can save up to $7 in future costs related to child welfare, healthcare, criminal justice, and lost productivity.")
        
        # End with call to action
        st.markdown("### Your Role in Prevention")
        st.markdown("""
        <div class="narrative-section">
            <p>Everyone has a role to play in preventing child maltreatment:</p>
            <ul>
                <li><strong>Community members</strong> can support family-friendly policies and resources</li>
                <li><strong>Educators and healthcare providers</strong> can learn to recognize and report warning signs</li>
                <li><strong>Policymakers</strong> can fund evidence-based prevention programs</li>
                <li><strong>Businesses</strong> can implement family-friendly policies</li>
                <li><strong>Individuals</strong> can volunteer with and donate to prevention organizations</li>
            </ul>
            <p>Together, we can create communities where all children are safe, supported, and able to thrive.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress completion
        st.success("You've completed the narrative journey! Now explore the data in detail in the other sections.")

# ------------------------------
# Data Explorer Page
# ------------------------------
elif page == "📊 Data Explorer":
    st.markdown('<div class="page-header">', unsafe_allow_html=True)
    st.title("Interactive Data Explorer")
    st.subheader("Understand the trends, patterns, and underlying story")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for different data views
    tab1, tab2, tab3 = st.tabs(["National Trends", "Demographic Analysis", "Reporting Sources"])
    
    with tab1:
        st.markdown("### National Trends in Child Maltreatment (2018-2022)")
        
        # Metric selection
        metric = st.radio(
            "Select metric to visualize",
            ["Total Victims", "Victimization Rate", "Fatalities", "Types of Maltreatment"],
            horizontal=True
        )
        
        trends_df = get_national_trends()
        
        if metric == "Total Victims":
            # Create area chart for victims
            fig = px.area(trends_df, x="Year", y="Victims",
                        labels={"Victims": "Number of Victims", "Year": "Year"},
                        color_discrete_sequence=["#6A8EAE"])
            
            fig.update_layout(
                title="Total Reported Victims by Year",
                height=500,
                hovermode="x unified"
            )
            
            # Add annotation for context
            fig.add_annotation(
                x=2020, y=650000,
                text="COVID-19 pandemic",
                showarrow=True,
                arrowhead=1
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show percentage change
            start_val = trends_df.iloc[0]["Victims"]
            end_val = trends_df.iloc[-1]["Victims"]
            pct_change = ((end_val - start_val) / start_val) * 100
            
            st.metric(
                label="Change 2018 to 2022",
                value=f"{pct_change:.1f}%",
                delta=f"{end_val - start_val:,} fewer victims"
            )
            
            # Key insight
            display_key_takeaway("The reduction in total victims may reflect better prevention, but could also be affected by changes in reporting processes and pandemic-related disruptions to normal detection channels like schools.")
            
        elif metric == "Victimization Rate":
            # Create synthetic victim rate data (per 1,000 children)
            rate_data = pd.DataFrame({
                "Year": trends_df["Year"],
                "Rate": [9.2, 8.9, 8.4, 8.1, 7.5]
            })
            
            fig = px.line(rate_data, x="Year", y="Rate", markers=True,
                        labels={"Rate": "Victimization Rate per 1,000 Children", "Year": "Year"},
                        color_discrete_sequence=["#FF9E7A"])
            
            fig.update_layout(
                title="Child Victimization Rate per 1,000 Children",
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Context and meaning
            st.markdown("""
            <div style="background-color: #F7F7F7; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <strong>What this means:</strong> The victimization rate represents the number of victims per 1,000 children in the population.
                This metric controls for changes in the total child population and provides a more standardized measure of maltreatment prevalence.
            </div>
            """, unsafe_allow_html=True)
            
            # Key insight
            display_key_takeaway("The declining victimization rate suggests real progress in prevention efforts, as this metric accounts for population changes.")
            
        elif metric == "Fatalities":
            fig = px.bar(trends_df, x="Year", y="Fatalities",
                       labels={"Fatalities": "Number of Fatalities", "Year": "Year"},
                       color_discrete_sequence=["#FF9E7A"])
            
            fig.update_layout(
                title="Child Maltreatment Fatalities by Year",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate fatality rate per 100,000 children (estimated)
            population_data = {
                2018: 73000000,
                2019: 72800000,
                2020: 72600000,
                2021: 72400000,
                2022: 72200000
            }
            
            fatality_rates = []
            for year, row in trends_df.iterrows():
                year_val = row["Year"]
                fatalities = row["Fatalities"]
                pop = population_data[year_val]
                rate = (fatalities / pop) * 100000
                fatality_rates.append({"Year": year_val, "Rate": rate})
            
            rate_df = pd.DataFrame(fatality_rates)
            
            fig2 = px.line(rate_df, x="Year", y="Rate", markers=True,
                         labels={"Rate": "Fatality Rate per 100,000 Children", "Year": "Year"},
                         color_discrete_sequence=["#6A8EAE"])
            
            fig2.update_layout(
                title="Child Fatality Rate per 100,000 Children",
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Key insight
            display_key_takeaway("The increase in fatalities, even as overall cases decline, highlights the critical need for better identification of high-risk situations and more effective interventions for the most vulnerable children.")
        
        elif metric == "Types of Maltreatment":
            # Create data for types over time (estimated trends)
            types_data = {
                "Year": [2018, 2019, 2020, 2021, 2022] * 5,
                "Type": ["Neglect"] * 5 + ["Physical Abuse"] * 5 + ["Sexual Abuse"] * 5 + ["Psychological Abuse"] * 5 + ["Other"] * 5,
                "Percentage": [
                    # Neglect
                    76.0, 75.5, 76.1, 75.0, 74.2,
                    # Physical Abuse
                    17.5, 17.2, 16.5, 16.9, 16.8,
                    # Sexual Abuse
                    7.3, 7.9, 8.1, 8.4, 8.5,
                    # Psychological
                    5.4, 5.6, 5.3, 5.5, 5.6,
                    # Other
                    1.8, 1.9, 2.0, 2.2, 2.1
                ]
            }
            
            types_df = pd.DataFrame(types_data)
            
            fig = px.area(types_df, x="Year", y="Percentage", color="Type", 
                        color_discrete_sequence=['#6A8EAE', '#7FB5B5', '#FF9E7A', '#C1E3A6', '#F9E9D9'],
                        groupnorm='percent')
            
            fig.update_layout(
                title="Proportions of Maltreatment Types by Year",
                height=500,
                hovermode="x unified",
                legend_title="Type of Maltreatment"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key insight
            display_key_takeaway("While neglect consistently remains the most common form of maltreatment, sexual abuse has shown a slight but concerning upward trend over the five-year period.")
    
    with tab2:
        st.markdown("### Demographic Analysis")
        
        # Age distribution visualization
        st.markdown("#### Age Distribution of Victims")
        
        age_data = get_age_breakdown()
        age_df = pd.DataFrame({
            "Age Group": list(age_data.keys()),
            "Number of Victims": list(age_data.values())
        })
        
        fig = px.bar(age_df, x="Age Group", y="Number of Victims",
                   color="Number of Victims",
                   color_continuous_scale=["#6A8EAE", "#FF9E7A"],
                   text="Number of Victims")
        
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        
        fig.update_layout(
            title="Victims by Age Group (2022)",
            height=500,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create visualization for risk by age
        risk_by_age = {
            "Age Group": list(age_data.keys()),
            "Rate per 1,000": [25.3, 12.2, 9.1, 7.5, 6.4, 5.7]
        }
        
        risk_df = pd.DataFrame(risk_by_age)
        
        fig2 = px.line(risk_df, x="Age Group", y="Rate per 1,000", markers=True,
                     labels={"Rate per 1,000": "Victimization Rate per 1,000 Children"},
                     color_discrete_sequence=["#FF9E7A"])
        
        fig2.update_layout(
            title="Victimization Rate by Age Group (2022)",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Key insight
        display_key_takeaway("The dramatic decline in victimization rates as age increases highlights the extreme vulnerability of infants and very young children, who depend entirely on caregivers and cannot report their own maltreatment.")
        
        # Race/ethnicity data
        st.markdown("#### Disparities by Race/Ethnicity")
        
        disparity_df = get_disparities_data()
        
        fig3 = px.bar(disparity_df, x="Race", y="Victim_Rate",
                    color="Victim_Rate",
                    color_continuous_scale=["#6A8EAE", "#7FB5B5", "#FF9E7A"],
                    text="Victim_Rate")
        
        fig3.update_traces(texttemplate='%{text}', textposition='outside')
        
        fig3.update_layout(
            title="Victimization Rate per 1,000 Children by Race/Ethnicity (2022)",
            height=500,
            coloraxis_showscale=False,
            yaxis_title="Rate per 1,000 Children"
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Contextual information
        st.markdown("""
        <div style="background-color: #F7F7F7; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <strong>Context for understanding disparities:</strong> These disparities reflect systemic inequities, including:
            <ul>
                <li>Unequal access to prevention and support resources</li>
                <li>Economic inequality</li>
                <li>Historical trauma</li>
                <li>Potential reporting and investigation biases</li>
            </ul>
            Effective prevention must address these underlying factors.
        </div>
        """, unsafe_allow_html=True)
        
        # Key insight
        display_key_takeaway("American Indian/Alaska Native children experience the highest victimization rates, highlighting the need for culturally-specific prevention approaches and addressing historical trauma.")
    
    with tab3:
        st.markdown("### Reporting Sources & System Response")
        
        # Create synthetic data for reporting sources
        reporting_data = {
            "Source": ["Education Personnel", "Legal & Law Enforcement", "Medical Personnel", 
                     "Social Services", "Mental Health", "Family/Friends/Neighbors", "Anonymous", "Other"],
            "Percentage": [21.5, 19.0, 11.7, 10.8, 8.3, 16.2, 8.0, 4.5]
        }
        
        report_df = pd.DataFrame(reporting_data)
        
        fig = px.pie(report_df, values="Percentage", names="Source",
                   color_discrete_sequence=['#6A8EAE', '#7FB5B5', '#9ECCAB', '#C1E3A6', '#F9E9D9', '#FFD1B8', '#FF9E7A', '#F0F0F0'],
                   hole=0.4)
        
        fig.update_layout(
            title="Sources of Child Maltreatment Reports (2022)",
            height=600
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insight
        display_key_takeaway("Education personnel are the largest source of reports, highlighting the crucial role of schools in identifying maltreatment. During COVID-19 school closures, many children lost this important safeguard.")
        
        # System response data
        st.markdown("#### System Response to Reports")
        
        # Create synthetic data for reports outcome
        outcome_data = {
            "Outcome": ["Screened-Out", "Unsubstantiated", "Substantiated", "Alternative Response"],
            "Percentage": [27.5, 34.9, 16.1, 21.5]
        }
        
        outcome_df = pd.DataFrame(outcome_data)
        
        fig2 = px.funnel(outcome_df, x="Percentage", y="Outcome",
                       color_discrete_sequence=['#FF9E7A', '#FFD1B8', '#6A8EAE', '#7FB5B5'])
        
        fig2.update_layout(
            title="Outcomes of Child Maltreatment Reports (2022)",
            height=500
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Contextual explanation
        st.markdown("""
        <div style="background-color: #F7F7F7; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <strong>Understanding the report pipeline:</strong>
            <ul>
                <li><strong>Screened-Out:</strong> Reports that don't meet criteria for investigation</li>
                <li><strong>Unsubstantiated:</strong> Investigated but insufficient evidence found</li>
                <li><strong>Substantiated:</strong> Investigation determined maltreatment occurred</li>
                <li><strong>Alternative Response:</strong> Family received services without determination</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Key insight
        display_key_takeaway("Only a small percentage of all reports result in substantiated findings, but alternative response approaches are increasingly being used to provide support to families without formal substantiation.")

# ------------------------------
# Geographic Insights Page
# ------------------------------
elif page == "🗺️ Geographic Insights":
    st.markdown('<div class="page-header">', unsafe_allow_html=True)
    st.title("Geographic Patterns")
    st.subheader("Explore how maltreatment rates vary across states")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Get state data
    state_df = get_state_data()
    
    # Column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Interactive Map of Child Maltreatment Statistics")
        
        # Metric to visualize
        map_metric = st.radio(
            "Select metric to visualize",
            ["Victim Count", "Victim Rate", "Fatalities"],
            horizontal=True
        )
        
        # Interactive folium map with better visualization
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="cartodbpositron")
        
        # Add state markers with scaled circles based on selected metric
        if map_metric == "Victim Count":
            # Create a marker cluster for better visualization
            marker_cluster = MarkerCluster().add_to(m)
            
            # Add proportional circles for each state
            for idx, row in state_df.iterrows():
                # Scale radius based on number of victims (min 10, max 50)
                radius = 10 + (row["Victims"] / 80000) * 40
                
                # Create circle marker
                folium.CircleMarker(
                    location=[row["Latitude"], row["Longitude"]],
                    radius=radius,
                    color="#6A8EAE",
                    fill=True,
                    fill_opacity=0.6,
                    popup=f"""
                    <strong>{row['State']}</strong><br>
                    Victims: {row['Victims']:,}<br>
                    Rate: {row['Victim_Rate']} per 1,000<br>
                    Fatalities: {row['Fatalities']}
                    """
                ).add_to(m)
        
        elif map_metric == "Victim Rate":
            # Create choropleth-like visualization with circles colored by rate
            for idx, row in state_df.iterrows():
                # Determine color based on victim rate
                if row["Victim_Rate"] < 5:
                    color = "#C1E3A6"  # Low rate - green
                elif row["Victim_Rate"] < 10:
                    color = "#F9E9D9"  # Medium rate - neutral
                else:
                    color = "#FF9E7A"  # High rate - coral/red
                
                # Create circle marker
                folium.CircleMarker(
                    location=[row["Latitude"], row["Longitude"]],
                    radius=15,
                    color=color,
                    fill=True,
                    fill_opacity=0.8,
                    popup=f"""
                    <strong>{row['State']}</strong><br>
                    Rate: {row['Victim_Rate']} per 1,000<br>
                    Victims: {row['Victims']:,}<br>
                    Fatalities: {row['Fatalities']}
                    """
                ).add_to(m)
        
        elif map_metric == "Fatalities":
            for idx, row in state_df.iterrows():
                # Scale radius based on fatalities
                radius = 10 + (row["Fatalities"] / 600) * 40
                
                # Create circle marker
                folium.CircleMarker(
                    location=[row["Latitude"], row["Longitude"]],
                    radius=radius,
                    color="#FF9E7A",
                    fill=True,
                    fill_opacity=0.6,
                    popup=f"""
                    <strong>{row['State']}</strong><br>
                    Fatalities: {row['Fatalities']}<br>
                    Victims: {row['Victims']:,}<br>
                    Rate: {row['Victim_Rate']} per 1,000
                    """
                ).add_to(m)
        
        # Add legend
        legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; 
        padding: 10px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <h4>Legend</h4>
        """
        
        if map_metric == "Victim Count" or map_metric == "Fatalities":
            legend_html += """
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="width: 20px; height: 20px; border-radius: 50%; background-color: #6A8EAE; margin-right: 5px;"></div>
                <div>Smaller Circle = Lower Value</div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #6A8EAE; margin-right: 5px;"></div>
                <div>Larger Circle = Higher Value</div>
            </div>
            """
        elif map_metric == "Victim Rate":
            legend_html += """
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="width: 20px; height: 20px; border-radius: 50%; background-color: #C1E3A6; margin-right: 5px;"></div>
                <div>Low Rate (< 5 per 1,000)</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="width: 20px; height: 20px; border-radius: 50%; background-color: #F9E9D9; margin-right: 5px;"></div>
                <div>Medium Rate (5-10 per 1,000)</div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; border-radius: 50%; background-color: #FF9E7A; margin-right: 5px;"></div>
                <div>High Rate (> 10 per 1,000)</div>
            </div>
            """
        
        legend_html += "</div>"
        
        # Add the legend to the map
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Display the map in Streamlit
        st_folium(m, width=700, height=500)
    
    with col2:
        st.markdown("### State Comparison")
        
        # State selection for comparison
        selected_states = st.multiselect(
            "Select states to compare",
            sorted(state_df["State"].unique()),
            default=["Massachusetts", "California"]
        )
        
        if selected_states:
            # Filter for selected states
            comparison_df = state_df[state_df["State"].isin(selected_states)]
            
            # Create comparison visualizations
            fig = px.bar(comparison_df, x="State", y="Victim_Rate", 
                       color="State",
                       labels={"Victim_Rate": "Victim Rate per 1,000 Children"},
                       title="Victim Rate Comparison")
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            fig2 = px.bar(comparison_df, x="State", y="Victims", 
                        color="State",
                        labels={"Victims": "Number of Victims"},
                        title="Victim Count Comparison")
            
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Key insight
        display_key_takeaway("Geographic patterns reveal significant variations in maltreatment rates across states, suggesting that policy differences, reporting practices, and socioeconomic factors all play important roles.")
    
    # State profile section
    st.markdown("---")
    st.markdown("### State Profile")
    
    # State selection
    selected_state = st.selectbox("Select a state to view detailed profile", sorted(state_df["State"].unique()))
    
    # Display state profile
    state_row = state_df[state_df["State"] == selected_state].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_stat_card("Victims", f"{state_row['Victims']:,}", f"In {selected_state}", "👧👦")
    
    with col2:
        create_stat_card("Victim Rate", f"{state_row['Victim_Rate']}", "Per 1,000 children", "📊")
    
    with col3:
        create_stat_card("Fatalities", f"{state_row['Fatalities']}", f"Child deaths", "💔")
    
    # State comparison to national average
    st.markdown(f"### How {selected_state} Compares to National Averages")
    
    # Create synthetic national averages
    national_avg = {
        "Victims": 558899 / 50,  # Divide by 50 states
        "Victim_Rate": 7.5,
        "Fatalities": 1990 / 50
    }
    
    # Create comparison metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        victim_diff = (state_row["Victims"] / national_avg["Victims"] - 1) * 100
        st.metric(
            label="Victim Count",
            value=f"{state_row['Victims']:,}",
            delta=f"{victim_diff:.1f}% than average"
        )
    
    with col2:
        rate_diff = (state_row["Victim_Rate"] / national_avg["Victim_Rate"] - 1) * 100
        st.metric(
            label="Victim Rate",
            value=f"{state_row['Victim_Rate']}",
            delta=f"{rate_diff:.1f}% than average"
        )
    
    with col3:
        fatality_diff = (state_row["Fatalities"] / national_avg["Fatalities"] - 1) * 100
        st.metric(
            label="Fatalities",
            value=f"{state_row['Fatalities']}",
            delta=f"{fatality_diff:.1f}% than average"
        )

# ------------------------------
# Understanding Disparities Page
# ------------------------------
elif page ==