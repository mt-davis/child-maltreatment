import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, display_fact_box, create_comparison_bar, create_tooltip
from utils.charts import create_bar_chart, create_donut_chart, create_bubble_chart
from data.data_loader import get_disparities_data, get_age_data

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - Disparities",
    page_icon="📉",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("Disparities in Child Maltreatment")
st.markdown("""
Child maltreatment does not affect all communities equally. This dashboard explores the disparities 
that exist across racial, ethnic, socioeconomic, and age groups.

Understanding these disparities is crucial for creating targeted prevention and intervention strategies 
that address the unique needs and challenges of different communities.
""")

# Load data
disparities_df = get_disparities_data()
age_df = get_age_data()

# Create tabs for different disparities
st.markdown("## Explore Different Types of Disparities")
tab1, tab2, tab3 = st.tabs(["Racial/Ethnic Disparities", "Age-Related Disparities", "Intersectional Analysis"])

with tab1:
    st.markdown("### Victimization Rate by Race/Ethnicity")
    st.markdown("""
    The data below shows the rate at which children of different racial and ethnic backgrounds
    experience substantiated maltreatment. These disparities reflect a complex interplay of factors
    including historical inequities, socioeconomic factors, reporting biases, and systemic issues.
    """)
    
    # Sort data by victimization rate for chart
    sorted_disparities = disparities_df.sort_values(by="Victim_Rate", ascending=False)
    
    # Create bar chart
    race_chart = create_bar_chart(
        sorted_disparities,
        "Race",
        "Victim_Rate",
        "Victimization Rate per 1,000 Children by Race/Ethnicity",
        color="#9b59b6"
    )
    
    st.altair_chart(race_chart, use_container_width=True)
    
    # Add context for disparities
    st.markdown("""
    #### Understanding These Disparities
    
    It's important to note that these disparities do not suggest inherent differences in parenting practices
    across racial or ethnic groups. Rather, they reflect:
    
    - **Historical and ongoing inequities** in access to resources and opportunities
    - **Socioeconomic factors** such as poverty, housing instability, and lack of access to healthcare
    - **Reporting biases** including potential over-scrutiny of certain communities
    - **Systemic and structural factors** that affect family stability and well-being
    
    Research consistently shows that when controlling for socioeconomic factors, racial
    disparities in maltreatment rates are significantly reduced.
    """)
    
    # Compare to population percentage
    st.markdown("### Context: Population Distribution vs. Victimization Rates")
    
    # Create a bubble chart to show both population percentage and victimization rate
    bubble_chart = create_bubble_chart(
        disparities_df,
        "Percent_Of_Population",
        "Victim_Rate",
        "Percent_Of_Population",  # Using this for size as well
        "Race",
        "Race/Ethnicity: Population Percentage vs. Victimization Rate"
    )
    
    st.altair_chart(bubble_chart, use_container_width=True)
    
    st.markdown("""
    This visualization shows the relationship between each group's percentage of the overall
    population (x-axis and bubble size) and their victimization rate (y-axis). This helps
    contextualize the impact of disparities on different communities.
    """)

with tab2:
    st.markdown("### Age-Related Disparities")
    
    # Sort age data by victimization rate for chart
    sorted_age = age_df.sort_values(by="Victim_Rate", ascending=False)
    
    # Create bar chart for age data
    age_chart = create_bar_chart(
        sorted_age,
        "Age_Group",
        "Victim_Rate",
        "Victimization Rate per 1,000 Children by Age Group",
        color="#f39c12"
    )
    
    st.altair_chart(age_chart, use_container_width=True)
    
    # Add context for age disparities
    st.markdown("""
    #### Why Young Children Are at Higher Risk
    
    The data clearly shows that younger children, particularly infants under one year old,
    experience maltreatment at significantly higher rates than older children. This vulnerability
    stems from several factors:
    
    - **Complete dependency** on caregivers for all basic needs
    - **Inability to report abuse** or seek help
    - **Developmental vulnerability** to injury
    - **Caregiver stress** associated with caring for infants and young children
    - **Lack of visibility** to mandatory reporters (e.g., not in school)
    """)
    
    # Visual representation of infant vulnerability
    st.markdown("### Infant Vulnerability in Context")
    
    # Calculate how many times higher the infant rate is compared to teenagers
    infant_rate = age_df[age_df["Age_Group"] == "<1 year"]["Victim_Rate"].values[0]
    teen_rate = age_df[age_df["Age_Group"] == "16-17 years"]["Victim_Rate"].values[0]
    times_higher = infant_rate / teen_rate
    
    st.markdown(f"""
    <div style="background-color: #fdedec; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h4 style="color: #e74c3c; margin-top: 0;">Infant Vulnerability</h4>
        <p>Children under age 1 experience maltreatment at a rate <strong>{times_higher:.1f}x higher</strong> 
        than teenagers aged 16-17.</p>
        
        <div style="display: flex; align-items: center; margin-top: 15px;">
            <div style="font-size: 3rem; margin-right: 10px;">👶</div>
            <div style="flex-grow: 1; height: 30px; background-color: #e74c3c; border-radius: 15px;"></div>
        </div>
        <p style="text-align: right; margin-top: 5px;">{infant_rate} per 1,000</p>
        
        <div style="display: flex; align-items: center; margin-top: 15px;">
            <div style="font-size: 3rem; margin-right: 10px;">🧑</div>
            <div style="width: {(teen_rate/infant_rate)*100}%; height: 30px; background-color: #e74c3c; border-radius: 15px;"></div>
        </div>
        <p style="text-align: right; margin-top: 5px;">{teen_rate} per 1,000</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("### Intersectional Analysis")
    st.markdown("""
    Child maltreatment risk factors often overlap and intersect. This analysis explores how
    different risk factors combine to create varying levels of vulnerability.
    
    > Note: The following visualization is a simplified representation as actual intersectional 
    > data with multiple variables is complex and not fully captured in aggregated statistics.
    """)
    
    # Create a simplified representation of intersectional factors
    # For an actual app, this would use real intersectional data
    
    # Create example data
    intersectional_data = pd.DataFrame({
        "Factor_Combination": [
            "Low income + Young parent", 
            "Low income + Substance abuse", 
            "Single parent + Low income", 
            "Low income + Social isolation",
            "Low income only",
            "Young parent only", 
            "Substance abuse only",
            "Single parent only",
            "Social isolation only"
        ],
        "Relative_Risk": [4.8, 4.2, 3.5, 3.2, 2.5, 1.8, 2.2, 1.5, 1.3],
        "Category": [
            "Multiple Factors", "Multiple Factors", "Multiple Factors", "Multiple Factors",
            "Single Factor", "Single Factor", "Single Factor", "Single Factor", "Single Factor"
        ]
    })
    
    # Create bar chart for intersectional data
    intersectional_chart = alt.Chart(intersectional_data).mark_bar().encode(
        x=alt.X("Relative_Risk:Q", title="Relative Risk of Maltreatment"),
        y=alt.Y("Factor_Combination:N", title=None, sort="-x"),
        color=alt.Color(
            "Category:N",
            scale=alt.Scale(
                domain=["Multiple Factors", "Single Factor"],
                range=["#c0392b", "#7f8c8d"]
            )
        ),
        tooltip=["Factor_Combination", "Relative_Risk", "Category"]
    ).properties(
        title="Intersectionality of Risk Factors (Simplified Representation)"
    ).interactive()
    
    st.altair_chart(intersectional_chart, use_container_width=True)
    
    st.markdown("""
    #### Understanding Intersectionality in Risk Factors
    
    This simplified representation illustrates an important concept: risk factors for child maltreatment
    rarely occur in isolation and often have a multiplicative rather than merely additive effect.
    
    For example, poverty alone increases risk, but when combined with social isolation or substance
    abuse, the risk increases disproportionately. This understanding helps in designing more
    effective, comprehensive prevention and intervention strategies.
    """)

# Policy implications section
st.markdown("## Policy and Practice Implications")

col1, col2 = st.columns(2)

with col1:
    display_fact_box(
        "Targeted Interventions", 
        "Understanding disparities allows for the development of targeted interventions that address the specific needs and challenges of different communities."
    )
    
    display_fact_box(
        "Resource Allocation", 
        "Data on disparities can inform how resources are allocated to ensure they reach the communities with the greatest need and vulnerability."
    )

with col2:
    display_fact_box(
        "Culturally Responsive Services", 
        "Effective services must be culturally responsive and designed with input from the communities they aim to serve."
    )
    
    display_fact_box(
        "Addressing Root Causes", 
        "Long-term solutions must address the systemic and structural factors that contribute to disparities, including poverty, housing instability, and access to healthcare."
    )

# Data sources and methodology
with st.expander("Data Sources & Methodology"):
    st.markdown("""
    ### Data Sources
    
    The disparities data presented in this dashboard is aggregated from several sources:
    
    - **Primary Source**: U.S. Department of Health & Human Services, Administration for Children and Families, Children's Bureau
    - National Child Abuse and Neglect Data System (NCANDS)
    - Census Bureau population estimates for demographic context
    - Research literature on risk factors and their interactions
    
    ### Methodology Notes
    
    - **Rate Calculations**: Victimization rates are calculated as the number of victims per 1,000 children in each specific population group
    - **Data Limitations**: Some demographic data may be incomplete in case reports
    - **Intersectional Analysis**: The intersectional analysis presented is a simplified representation based on research literature, as comprehensive intersectional data is limited
    - **Causal Interpretation**: Disparities should not be interpreted as causal or deterministic; they reflect complex societal factors
    
    For more detailed methodology information, please refer to the original reports.
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")