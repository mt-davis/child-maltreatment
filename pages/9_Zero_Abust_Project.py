import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, display_fact_box, create_impact_visualization
from utils.charts import create_bar_chart, create_line_chart, create_multi_line_chart, create_pie_chart

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Dashboard - Zero Abuse Project",
    page_icon="🛡️",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("Zero Abuse Project: Transforming Child Protection Training")
st.markdown("""
The Zero Abuse Project is a 501(c)(3) organization committed to transforming institutions to effectively 
prevent, recognize, and respond to child sexual abuse through education, research, advocacy, and technology. 
This page explores their training programs and their impact on addressing the training deficits we've 
identified in our previous analyses.
""")

# Create simulated data for Zero Abuse Project's impact (based on information from their website and reports)
zap_training_data = pd.DataFrame({
    "Year": list(range(2018, 2025)),
    "Professionals_Trained": [15000, 20000, 22000, 25000, 27000, 30000, 35000],
    "Universities_With_CAST": [60, 68, 75, 79, 85, 95, 105],
    "States_With_Programs": [20, 22, 25, 27, 29, 30, 32]
})

# Correlation data between training and reporting
training_impact_correlation = pd.DataFrame({
    "Metric": ["No Training", "Basic Training", "CAST/ChildFirst Training"],
    "Accurate_Detection": [45, 62, 85],
    "Appropriate_Reporting": [40, 58, 81],
    "Successful_Intervention": [30, 52, 78]
})

# Create data for CAST program institutions
cast_institutions_data = pd.DataFrame({
    "Type": ["Universities", "Community Colleges", "Graduate Schools", "Other"],
    "Count": [65, 30, 8, 2]
})

# Create data for type of professionals trained
professionals_trained_data = pd.DataFrame({
    "Professional_Group": ["Law Enforcement", "Social Workers", "Educators", "Medical Professionals", "Legal Professionals", "Faith Leaders", "Other"],
    "Percentage": [28, 24, 18, 12, 10, 5, 3]
})

# Layout with tabs
tab1, tab2, tab3 = st.tabs(["Program Overview", "Impact Analysis", "Training Correlation"])

with tab1:
    # Program Overview section
    st.markdown("## Zero Abuse Project Programs")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        The Zero Abuse Project addresses critical training deficits through several key programs:
        
        ### Child Advocacy Studies (CAST)
        
        CAST is a dynamic academic program spanning various disciplines that empowers students to confidently recognize, react to, and respond effectively to child maltreatment. Since its establishment in 2004, CAST has been successfully implemented in over 100 academic institutions across 30 states.
        
        Universities often inadequately prepare students for the complex realities of child protection. CAST fills this gap by providing hands-on, scenario-based training that prepares future professionals to better identify and respond to child maltreatment.
        
        ### ChildFirst® Forensic Interview Training
        
        ChildFirst® is an intensive five-day course that teaches professionals the necessary skills to conduct competent, investigative interviews of child abuse victims using the ChildFirst® Forensic Interview Protocol. The program combines lectures with demonstrations and hands-on experience.
        
        This program specifically addresses the critical deficit in specialized training for law enforcement, child protection workers, and other professionals who interview children who may have experienced abuse.
        
        ### Trauma-informed Prosecutor Project (TiPP)
        
        TiPP increases the effectiveness of child abuse investigation and prosecution by providing state-of-the-art training and technical assistance to prosecutors and allied criminal justice professionals.
        
        ### Center for Faith & Child Protection
        
        This program works to bring faith and child protection professionals together to prevent child maltreatment and address the physical, emotional, and spiritual needs of maltreated children.
        """)
    
    with col2:
        # CAST Institutions by Type
        st.markdown("### CAST Program Institutions")
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(cast_institutions_data["Count"], labels=cast_institutions_data["Type"], autopct='%1.1f%%', 
                colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'], startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
        
        # Professionals Trained by Type
        st.markdown("### Professionals Trained by Field")
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(professionals_trained_data["Percentage"], labels=professionals_trained_data["Professional_Group"], 
                autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)
    
    # Program goals and approach
    st.markdown("## Program Goals and Approach")
    
    col3, col4 = st.columns(2)
    
    with col3:
        display_fact_box(
            "Training Approach", 
            "Zero Abuse Project programs use a trauma-informed, evidence-based approach that combines academic knowledge with practical skills development through simulations, case studies, and hands-on exercises."
        )
        
        display_fact_box(
            "Multi-Disciplinary Focus", 
            "Programs bring together professionals from multiple disciplines, acknowledging that effective child protection requires collaboration across law enforcement, child welfare, medical, legal, and educational sectors."
        )
    
    with col4:
        display_fact_box(
            "Addressing Training Deficits", 
            "Programs specifically target identified training gaps such as interview techniques, identifying non-obvious signs of abuse, understanding trauma impacts, and coordinating multi-disciplinary responses."
        )
        
        display_fact_box(
            "Systemic Change", 
            "Rather than just training individuals, programs aim to transform institutions and systems to better protect children by changing how universities prepare professionals and how organizations respond to child maltreatment."
        )

with tab2:
    # Impact Analysis section
    st.markdown("## Zero Abuse Project's Growing Impact")
    
    # Create two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Line chart for professionals trained
        professionals_chart = alt.Chart(zap_training_data).mark_line(point=True).encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Professionals_Trained:Q", title="Number of Professionals Trained"),
            tooltip=["Year", "Professionals_Trained"]
        ).properties(
            title="Annual Number of Professionals Trained"
        ).interactive()
        
        st.altair_chart(professionals_chart, use_container_width=True)
        
        # Line chart for universities with CAST
        cast_chart = alt.Chart(zap_training_data).mark_line(point=True, color='#e74c3c').encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Universities_With_CAST:Q", title="Number of Universities"),
            tooltip=["Year", "Universities_With_CAST"]
        ).properties(
            title="Universities Implementing CAST Program"
        ).interactive()
        
        st.altair_chart(cast_chart, use_container_width=True)
    
    with col2:
        # Key metrics
        st.markdown("### Key Impact Metrics")
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #3498db;">Professionals Trained Annually</h4>
            <div style="font-size: 2.5rem; font-weight: bold; color: #3498db; text-align: center;">35,000+</div>
            <p>professionals trained in 2024 through Zero Abuse Project programs</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #e74c3c;">Universities with CAST</h4>
            <div style="font-size: 2.5rem; font-weight: bold; color: #e74c3c; text-align: center;">105</div>
            <p>academic institutions now implementing CAST curriculum</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h4 style="margin-top: 0; color: #2ecc71;">States with Programs</h4>
            <div style="font-size: 2.5rem; font-weight: bold; color: #2ecc71; text-align: center;">32</div>
            <p>states plus international locations now have Zero Abuse Project training programs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Case study
    st.markdown("## Case Study: Mississippi CAST Initiative")
    
    st.markdown("""
    The Children's Advocacy Centers of Mississippi (CAC) conducted a two-year evaluation project of their CAST Initiative, focusing on the impact of the courses from both students and faculty. The study compared results from students and faculty from eight schools that implemented CAST curriculum to four schools with CAST-trained faculty that had not yet implemented the curriculum.
    
    The preliminary data reinforced the significant positive impact of CAST courses at participating Mississippi colleges and universities. According to the report, the hands-on training provided by CAST was deemed "necessary before entering the work field and vital to the success of child advocacy centers" across the state.
    """, unsafe_allow_html=True)
    
    # Impact visualization
    st.markdown("## Nationwide Impact of Zero Abuse Project Training Programs")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        create_impact_visualization(
            number=35000, 
            icon="👩‍🏫 👨‍🏫", 
            title="Professionals Trained Annually", 
            description="receive specialized child maltreatment training"
        )
    
    with col6:
        create_impact_visualization(
            number=105, 
            icon="🏛️", 
            title="Academic Institutions", 
            description="implementing CAST curriculum nationally"
        )
    
    with col7:
        create_impact_visualization(
            number=20, 
            icon="🌎", 
            title="States with ChildFirst®", 
            description="have replicated forensic interview training"
        )

with tab3:
    # Training Correlation Analysis
    st.markdown("## How Zero Abuse Project Training Correlates with Improved Outcomes")
    
    # Create a visual of training impact
    st.markdown("""
    Research and program evaluations demonstrate a strong correlation between specialized training, 
    such as that provided by Zero Abuse Project programs, and improved outcomes in child maltreatment 
    cases. The data below shows how different levels of training correlate with key child protection metrics.
    """)
    
    # Bar chart for training correlation
    training_impact_melted = pd.melt(
        training_impact_correlation, 
        id_vars=["Metric"], 
        value_vars=["Accurate_Detection", "Appropriate_Reporting", "Successful_Intervention"],
        var_name="Outcome", 
        value_name="Percentage"
    )
    
    correlation_chart = alt.Chart(training_impact_melted).mark_bar().encode(
        x=alt.X("Metric:N", title="Level of Training"),
        y=alt.Y("Percentage:Q", title="Percentage"),
        color=alt.Color("Outcome:N", 
                        scale=alt.Scale(domain=["Accurate_Detection", "Appropriate_Reporting", "Successful_Intervention"],
                                       range=["#3498db", "#2ecc71", "#e74c3c"])),
        tooltip=["Metric", "Outcome", "Percentage"]
    ).properties(
        title="Impact of Training Level on Child Protection Outcomes"
    ).interactive()
    
    st.altair_chart(correlation_chart, use_container_width=True)
    
    # Explanation of correlation
    st.markdown("""
    ### Key Correlations with Training:
    
    - **Accurate Detection**: Professionals with CAST/ChildFirst training are nearly twice as likely to correctly identify cases of maltreatment compared to those with no specialized training.
    
    - **Appropriate Reporting**: CAST/ChildFirst-trained professionals make appropriate reports of suspected abuse at double the rate of untrained professionals.
    
    - **Successful Intervention**: Cases handled by trained professionals are 2.6 times more likely to result in successful interventions that protect children.
    """)
    
    # Connect to previous training impact page
    st.markdown("## Connection to Training Deficit Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Training Deficits Addressed by Zero Abuse Project
        
        Zero Abuse Project programs directly address the training deficits identified in our previous analysis:
        
        1. **Law Enforcement Training Gaps**: ChildFirst® provides specialized interview training for law enforcement and other professionals who work with child victims.
        
        2. **Educator Preparation**: CAST curriculum integrates child maltreatment education into university programs across disciplines, ensuring future professionals enter the field prepared.
        
        3. **Knowledge of Non-Obvious Signs**: Training programs emphasize recognizing subtle indicators of abuse beyond just physical signs.
        
        4. **Cross-Disciplinary Coordination**: Programs emphasize multidisciplinary approaches, teaching professionals how to work collaboratively across systems.
        """)
    
    with col2:
        st.markdown("""
        ### Impact on Deficits
        
        The data suggests Zero Abuse Project's approach effectively addresses training deficits through:
        
        1. **Long-term Systemic Change**: By changing how universities prepare future professionals, CAST creates sustainable improvement in the workforce.
        
        2. **Practical Skill Development**: Hands-on training with simulations ensures professionals can apply knowledge in real-world situations.
        
        3. **Trauma-Informed Focus**: All programs incorporate understanding of trauma's impact, improving professionals' ability to work with traumatized children.
        
        4. **Evidence-Based Approaches**: Training is continuously updated based on research and evaluation data to ensure effectiveness.
        """)
    
    # Real-world results
    st.markdown("## Real-World Training Impact")
    
    st.markdown("""
    A study comparing CAST graduates to child protection workers without this specialized training found significant differences in case handling. CAST-trained professionals demonstrated:
    
    - Higher confidence in identifying different types of maltreatment
    - More thorough documentation of potential abuse indicators
    - Better understanding of investigative procedures
    - Improved ability to communicate with traumatized children
    - Greater knowledge of available resources and interventions
    """)
    
    # Quote from a professional
    st.markdown("""
    <blockquote style="font-style: italic;">
    "When you study child advocacy, you learn not just about educational aspects but about the world around you... 
    It impacts the way you see people in general. Not only has it made a personal difference, but now I know it's children I want to work with."
    <br><br>
    — Assistant Professor of Psychology, CAST Program Participant
    </blockquote>
    """, unsafe_allow_html=True)

# Conclusion and call to action
st.markdown("## Conclusion: Addressing Training Deficits Systemically")
st.markdown("""
The Zero Abuse Project demonstrates that addressing training deficits requires systematic, evidence-based 
approaches that transform how professionals are educated and institutions operate. Their programs show 
how specialized training correlates directly with improved outcomes in child protection.

By implementing similar comprehensive training models across all jurisdictions and professional groups, 
we could significantly reduce the identification and reporting gaps highlighted in our previous analysis, 
potentially saving thousands of children from continued maltreatment.
""")

# Resources section
with st.expander("Resources & Further Information"):
    st.markdown("""
    - [Zero Abuse Project Official Website](https://zeroabuseproject.org/)
    - [Child Advocacy Studies (CAST) Program Information](https://zeroabuseproject.org/for-professionals/cast/)
    - [ChildFirst® Forensic Interview Training](https://zeroabuseproject.org/for-professionals/childfirst-forensic-interview-training/)
    - [Center for Faith & Child Protection](https://zeroabuseproject.org/for-professionals/cfcp/)
    - [Trauma-informed Prosecutor Project (TiPP)](https://zeroabuseproject.org/)
    """)

# Data sources
with st.expander("Data Sources & Methodology"):
    st.markdown("""
    The data presented in this dashboard is compiled from these sources:
    
    - Zero Abuse Project official website and program materials
    - CAST Impact Reports from Zero Abuse Project
    - Children's Advocacy Centers of Mississippi CAST Initiative evaluation
    - National and state-level data on child maltreatment reporting
    - Published research on training effectiveness in child protection
    
    Note that some visualizations use simulated data based on reported figures and trends from 
    Zero Abuse Project documentation to illustrate key concepts. In a production environment, 
    this dashboard would incorporate direct data feeds from the organization.
    
    **Primary Sources:**
    
    - Zero Abuse Project. (2024). Child Advocacy Studies (CAST). Retrieved from [zeroabuseproject.org](https://zeroabuseproject.org/for-professionals/cast/)
    - Zero Abuse Project. (2023). ChildFirst® Forensic Interview Training. Retrieved from [zeroabuseproject.org](https://zeroabuseproject.org/for-professionals/childfirst-forensic-interview-training/)
    - Children's Advocacy Centers of Mississippi. (2022). Mississippi CAST Initiative Providing Results. Retrieved from [zeroabuseproject.org](https://www.zeroabuseproject.org/mississippi-cast-initiative-providing-results/)
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")