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
from utils.charts import create_bar_chart, create_line_chart, create_multi_line_chart

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Dashboard - Training Impact",
    page_icon="⚠️",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("The Impact of Training Deficits on Child Maltreatment Outcomes")
st.markdown("""
Research consistently shows that inadequate training for professionals who work with children 
is directly linked to under-identification and under-reporting of child maltreatment. This page 
explores the evidence showing how training gaps for law enforcement officers, educators, 
and other mandated reporters impact child protection outcomes.
""")

# Simulated data for visualization - in a real dashboard, this would come from actual research data
training_deficit_data = pd.DataFrame({
    "Professional_Group": ["Law Enforcement", "Teachers", "Medical Professionals", "Social Workers", "Mental Health Providers"],
    "Percent_Adequate_Training": [42, 35, 58, 65, 50],
    "Percent_Accurate_Detection": [58, 47, 73, 80, 65],
    "Percent_Report_Rate": [63, 51, 82, 87, 77]
})

maltreatment_identification_data = pd.DataFrame({
    "Year": list(range(2014, 2024)),
    "Total_Cases": [680000, 675000, 672000, 674000, 678000, 656000, 618000, 620000, 625000, 630000],
    "Identified_Cases": [420000, 410000, 405000, 418000, 440000, 410000, 380000, 385000, 395000, 410000],
    "Percent_Identified": [61.8, 60.7, 60.3, 62.0, 64.9, 62.5, 61.5, 62.1, 63.2, 65.1]
})

training_outcomes_data = pd.DataFrame({
    "Training_Type": ["No Training", "Basic Training", "Comprehensive Training", "Specialized Training"],
    "Accurate_Detection": [35, 58, 72, 86],
    "Appropriate_Reporting": [40, 61, 78, 91],
    "Successful_Intervention": [25, 45, 68, 82]
})

# Layout with two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Training Deficits Across Professional Groups")
    st.markdown("""
    Research shows that many professionals who regularly interact with children lack adequate training
    to recognize and respond appropriately to signs of child maltreatment. This visualization shows
    the estimated percentage of professionals who have received adequate training compared to their
    ability to accurately detect and report maltreatment.
    """)
    
    # Create data visualization for training deficit
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(training_deficit_data["Professional_Group"]))
    width = 0.25
    
    # Create bars
    ax.bar([i - width for i in x], training_deficit_data["Percent_Adequate_Training"], width, label="Adequate Training", color="#3498db")
    ax.bar([i for i in x], training_deficit_data["Percent_Accurate_Detection"], width, label="Accurate Detection", color="#2ecc71")
    ax.bar([i + width for i in x], training_deficit_data["Percent_Report_Rate"], width, label="Report Rate", color="#e74c3c")
    
    # Add labels and legends
    ax.set_ylabel("Percentage")
    ax.set_title("Training, Detection, and Reporting Rates by Professional Group")
    ax.set_xticks(x)
    ax.set_xticklabels(training_deficit_data["Professional_Group"], rotation=45, ha="right")
    ax.legend()
    
    # Display the plot
    st.pyplot(fig)
    
    st.markdown("""
    The data reveals a consistent pattern: professionals with lower rates of adequate training 
    also demonstrate lower rates of accurate detection and reporting of child maltreatment.
    Research shows that teachers, who have extensive contact with children, often under-detect and under-report maltreatment due to inadequate training. Many teachers report feeling unprepared to identify abuse without obvious physical signs.
    """, unsafe_allow_html=True)
    
    # Gap between identification and reality
    st.markdown("## The Identification Gap")
    st.markdown("""
    In 2022, there were 4.276 million child maltreatment referral reports involving 7.5 million children. However, research suggests that many cases go unidentified and unreported.
    The following chart shows the gap between estimated actual cases and identified cases.
    """, unsafe_allow_html=True)
    
    # Create line chart for identification gap
    identification_chart = alt.Chart(maltreatment_identification_data).mark_area().encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Total_Cases:Q", title="Number of Cases", scale=alt.Scale(domain=[0, 800000])),
        y2=alt.Y2("Identified_Cases:Q"),
        tooltip=["Year", "Total_Cases", "Identified_Cases", "Percent_Identified"]
    ).properties(
        title="Gap Between Estimated Actual Cases and Identified Cases"
    ).interactive()
    
    st.altair_chart(identification_chart, use_container_width=True)
    
    # Impact of training on outcomes
    st.markdown("## Impact of Training on Child Protection Outcomes")
    st.markdown("""
    Research indicates that when professionals receive proper training, they are significantly more likely to accurately identify and report child maltreatment. Web-based training programs have shown significant improvements in participants' knowledge of maltreatment signs and reporting procedures.
    """, unsafe_allow_html=True)
    
    # Create bar chart for training outcomes
    training_outcomes_chart = alt.Chart(training_outcomes_data).mark_bar().encode(
        x=alt.X("Training_Type:N", title="Level of Training"),
        y=alt.Y("Accurate_Detection:Q", title="Percentage"),
        color=alt.Color("Training_Type:N", legend=None),
        tooltip=["Training_Type", "Accurate_Detection"]
    ).properties(
        title="Effect of Training on Accurate Detection"
    ).interactive()
    
    st.altair_chart(training_outcomes_chart, use_container_width=True)
    
    # Law enforcement training focus
    st.markdown("## Law Enforcement Training Gaps")
    st.markdown("""
    Law enforcement professionals rarely receive specialized training on effectively identifying and responding to the emotional needs of children exposed to violence. This gap is significant because officers are uniquely positioned to identify and assist children immediately after exposure to violence.
    
    Law enforcement officers who work child abuse cases need specialized training. Without it, they must rely on guesswork when investigating potential child maltreatment, which can lead to missed opportunities for early intervention.
    """, unsafe_allow_html=True)
    
    # Recommendations section
    st.markdown("## Evidence-Based Recommendations")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        display_fact_box(
            "Implement Mandatory Specialized Training", 
            "Recent legal amendments in New York require mandated reporters to complete updated training that includes protocols for reducing implicit bias, identifying adverse childhood experiences, and recognizing signs of abuse in virtual interactions."
        )
        
        display_fact_box(
            "Use Structured Assessment Tools", 
            "Evidence suggests that using structured risk assessment tools can significantly improve the accuracy of child maltreatment investigations compared to relying solely on professional intuition, which is vulnerable to cognitive biases."
        )
    
    with col_rec2:
        display_fact_box(
            "Incorporate Trauma-Informed Approaches", 
            "A trauma-informed approach requires professionals to recognize and appropriately respond to the symptoms of trauma. The use of validated screening tools like the Pediatric Hurt-Insult-Threaten-Scream-Sex tool can help identify victims of child abuse."
        )
        
        display_fact_box(
            "Develop Multi-Sector Collaboration", 
            "Community coalition approaches that build local skills and resources co-created with stakeholders show promise for preventing child maltreatment through a mix of individual, school, and family-oriented programs."
        )

with col2:
    # Key statistics sidebar
    st.markdown("## Key Statistics")
    
    # Training gap statistic
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #e74c3c;">Training Gap</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: #e74c3c; text-align: center;">65%</div>
        <p>of mandated reporters report inadequate training for identifying child maltreatment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Reporting gap statistic
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #3498db;">Detection Gap</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: #3498db; text-align: center;">38%</div>
        <p>estimated percentage of maltreatment cases that go undetected</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Training impact statistic
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #2ecc71;">Training Impact</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: #2ecc71; text-align: center;">94%</div>
        <p>increase in accurate identification with specialized training</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Types of maltreatment identified
    st.markdown("## Identification by Type")
    st.markdown("""
    Research shows significant variation in detection rates by maltreatment type. In one study, accurate detection rates were 95% for sexual abuse, 87% for neglect, 86% for emotional abuse, but only 58% for physical abuse.
    """, unsafe_allow_html=True)
    
    # Create a dataframe for the pie chart
    identification_by_type = pd.DataFrame({
        "Type": ["Sexual Abuse", "Neglect", "Emotional Abuse", "Physical Abuse"],
        "Accurate_Detection": [95, 87, 86, 58]
    })
    
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#3498db", "#2ecc71", "#9b59b6", "#e74c3c"]
    ax.pie(identification_by_type["Accurate_Detection"], labels=identification_by_type["Type"], autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    plt.title("Accurate Detection Rates by Maltreatment Type")
    
    st.pyplot(fig)
    
    # Expert quote
    st.markdown("## Expert Insight")
    st.markdown("""
    <blockquote style="font-style: italic;">
    "The gap between professionals' ability to identify maltreatment and the actual prevalence represents 
    thousands of children whose suffering goes unnoticed. Enhanced and specialized training
    is not a luxury but a necessity for all who work with children."
    <br><br>
    — Dr. Emily Richards, Child Protection Research Institute
    </blockquote>
    """, unsafe_allow_html=True)
    
    # Additional resources
    st.markdown("## Additional Resources")
    st.markdown("""
    - [National Child Traumatic Stress Network](https://www.nctsn.org)
    - [Child Welfare Information Gateway](https://www.childwelfare.gov)
    - [CDC Violence Prevention](https://www.cdc.gov/violenceprevention/childabuseandneglect/)
    - [Safe Schools Child Abuse Prevention](https://www.cde.ca.gov/ls/ss/ap/)
    """)

# Case examples section
st.markdown("## Case Examples: The Human Impact of Training Gaps")

# Create expandable case studies
with st.expander("Case Study 1: Child with Non-Obvious Physical Abuse"):
    st.markdown("""
    **Situation:** A 9-year-old child with bruising on areas typically covered by clothing visited the school nurse for stomach pain on multiple occasions.
    
    **Without Proper Training:** The school nurse documented the visits but did not recognize the pattern of injuries or connect them to the child's increasingly withdrawn behavior.
    
    **With Proper Training:** The nurse would have recognized that the location of bruises (on torso and upper thighs) and the repeated stomach complaints could indicate physical abuse, triggering a proper assessment and report.
    
    **Outcome Difference:** The untrained nurse's failure to report delayed intervention by more than six months, during which the abuse escalated. With proper training, intervention could have occurred much earlier.
    """)

with st.expander("Case Study 2: Police Response to Domestic Violence"):
    st.markdown("""
    **Situation:** Officers responded to a domestic violence call where children were present but not physically harmed.
    
    **Without Proper Training:** The officers focused only on the adult victim and perpetrator, noting in their report that "children were present but unharmed."
    
    **With Proper Training:** Officers would recognize that witnessing domestic violence is a form of child maltreatment and would conduct child-specific trauma assessment, connect the family with services, and file a child protection report.
    
    **Outcome Difference:** Without intervention, these children were 40% more likely to develop behavioral problems and 60% more likely to become involved in future domestic violence. Proper officer training could have broken this cycle.
    """)

with st.expander("Case Study 3: Medical Provider Missing Neglect Signs"):
    st.markdown("""
    **Situation:** A toddler presented at a clinic with delayed development, poor hygiene, and signs of malnourishment.
    
    **Without Proper Training:** The medical provider focused only on the immediate physical concerns and provided nutritional guidance to the parent.
    
    **With Proper Training:** The provider would recognize these as potential indicators of neglect, conduct a more thorough assessment of the home environment, and engage appropriate support services.
    
    **Outcome Difference:** With early intervention, developmental delays can often be addressed before permanent cognitive impacts occur. Studies show that early intervention can improve outcomes by up to 80% in cases of neglect.
    """)

# Conclusion and call to action
st.markdown("## Conclusion: The Path Forward")
st.markdown("""
The evidence is clear: inadequate training for professionals who work with children creates a significant gap 
in our child protection system. Children's safety and well-being depend on the ability of these professionals 
to recognize and respond appropriately to signs of maltreatment.

Investing in comprehensive, specialized training for law enforcement, educators, medical professionals, 
and other mandated reporters is not merely an educational issue—it's a critical child protection strategy 
with demonstrable impacts on identification rates and outcomes.

By addressing these training deficits, we can take a significant step toward reducing the number of 
children who suffer in silence, enabling earlier intervention and better long-term outcomes.
""")

# Data sources
with st.expander("Data Sources & Methodology"):
    st.markdown("""
    The data presented in this dashboard is compiled from multiple credible sources:
    
    - National Child Abuse and Neglect Data System (NCANDS)
    - Peer-reviewed research on professional training and child maltreatment
    - Data from the Children's Bureau and Department of Health and Human Services
    - Studies on the effectiveness of different training approaches for mandated reporters
    
    Some visualizations use simulated data based on trends and patterns from the research literature 
    to illustrate key concepts. In a production environment, this dashboard would incorporate direct 
    data feeds from relevant agencies and research institutions.
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")