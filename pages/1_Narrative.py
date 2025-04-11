import streamlit as st
import pandas as pd
import altair as alt
import time
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, create_story_container, display_fact_box, create_quote_box, highlight_stat, generate_random_story
from utils.charts import create_line_chart, create_area_chart
from data.data_loader import get_national_trends, get_quotes, get_age_data

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - Narrative",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("The Story Behind the Numbers")

# Introduction
st.markdown("""
Child maltreatment affects thousands of lives each year in the United States. 
While official reports show some improvement over time, the impact on the most vulnerable—especially infants—remains profound.

In this narrative exploration, we'll walk you through the data to reveal the human side of the numbers, 
explain the challenges, and highlight why continued effort and prevention are essential.
""")

# Main content in two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Overview section with key statistics
    st.markdown("## The Big Picture")
    
    # Use a slider to let the user explore different years
    trends_df = get_national_trends()
    year = st.slider("Select a Year to Explore", 
                    min(trends_df["Year"]), 
                    max(trends_df["Year"]), 
                    max(trends_df["Year"]))
    
    data_year = trends_df[trends_df["Year"] == year].iloc[0]
    
    # Create a visualization that updates with the slider
    st.markdown(f"""
    **In {year}:** There were **{data_year['Victims']:,}** reported cases of child maltreatment 
    and **{data_year['Fatalities']:,}** child fatalities nationwide.
    
    That's a victimization rate of **{data_year['Victim_Rate']} per 1,000 children**.
    """)
    
    # Chart for selected year with breakdown
    # Create a dataframe for the chart
    breakdown_data = pd.DataFrame({
        'Category': ['Neglect', 'Physical Abuse', 'Sexual Abuse', 'Other'],
        'Percentage': [
            data_year['Neglect_Percent'], 
            data_year['Physical_Abuse_Percent'], 
            data_year['Sexual_Abuse_Percent'],
            100 - (data_year['Neglect_Percent'] + data_year['Physical_Abuse_Percent'] + data_year['Sexual_Abuse_Percent'])
        ]
    })
    
    # Create the chart
    breakdown_chart = alt.Chart(breakdown_data).mark_bar().encode(
        x=alt.X('Percentage:Q', title='Percentage'),
        y=alt.Y('Category:N', title='Type of Maltreatment', sort='-x'),
        color=alt.Color('Category:N', scale=alt.Scale(
            domain=['Neglect', 'Physical Abuse', 'Sexual Abuse', 'Other'],
            range=['#3498db', '#e74c3c', '#9b59b6', '#95a5a6']
        )),
        tooltip=['Category', 'Percentage']
    ).properties(
        title=f'Types of Maltreatment in {year}'
    ).interactive()
    
    st.altair_chart(breakdown_chart, use_container_width=True)

    # What does this mean section
    st.markdown("## What Does This Mean?")
    col_a, col_b = st.columns(2)
    
    with col_a:
        display_fact_box("Reduction and Reality", 
                        "Even with a decline in overall cases, each number represents a child whose life was affected. Behind every statistic is a personal story of trauma and resilience.")
    
    with col_b:
        display_fact_box("The Unheard Pain", 
                        "Fatalities remain high, reminding us that for the youngest children, every loss is a failure of the support system designed to protect them.")
    
    # Story element
    create_story_container(
        generate_random_story(year=year), 
        "A Child's Experience"
    )
    
    # Age data
    st.markdown("## Children at Greatest Risk")
    st.markdown("""
    Not all children face the same level of risk. As the data shows, the youngest children—especially infants—are the most vulnerable to maltreatment.
    """)
    
    age_data = get_age_data()
    age_chart = alt.Chart(age_data).mark_bar().encode(
        x=alt.X('Victim_Rate:Q', title='Victimization Rate per 1,000 Children'),
        y=alt.Y('Age_Group:N', title='Age Group', sort='-x'),
        color=alt.Color('Victim_Rate:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['Age_Group', 'Victim_Rate']
    ).properties(
        title='Victimization Rate by Age Group'
    ).interactive()
    
    st.altair_chart(age_chart, use_container_width=True)
    
    st.markdown("""
    **Why are infants at such high risk?**
    * Their complete dependency on caregivers
    * Inability to verbalize or report maltreatment
    * The stress that a new baby can place on unprepared or under-resourced families
    * Fragility and vulnerability to physical injury
    """)
    
    # Hope and Urgency section
    st.markdown("## Hope and Urgency")
    st.markdown("""
    The data shows that progress is possible but requires sustained effort. Prevention initiatives that support families 
    before crises occur have shown promising results across the country.
    """)
    
    # Visualizing progress animation
    st.markdown("### Visualizing Progress Over Time")
    st.markdown("Imagine the progress we can achieve when every stakeholder commits to protecting our children.")
    progress_bar = st.progress(0)
    for percent in range(0, 101, 10):
        progress_bar.progress(percent)
        time.sleep(0.05)  # animation delay
    
    # Call to action
    st.markdown("""
    ## Our Call to Action  
    
    While the numbers tell us where we stand, they also remind us of our responsibility to keep working for meaningful change. 
    Every improvement in these statistics represents a step toward a safer future for our children.
    
    As you explore the other sections of this dashboard, remember that prevention is possible, and early intervention saves lives.
    """)

with col2:
    # Sidebar with survivor quotes and additional context
    st.markdown("## Survivor Voices")
    quotes = get_quotes()
    # Display 2-3 random quotes
    import random
    for quote in random.sample(quotes, 2):
        create_quote_box(
            quote['quote'],
            quote['name'],
            f"Age {quote['age']} - {quote['background']}"
        )
    
    # National trends mini chart
    st.markdown("## Trends at a Glance")
    victims_chart = create_area_chart(
        trends_df, 
        'Year', 
        'Victims', 
        'Child Maltreatment Victims Over Time',
        '#3498db'
    )
    st.altair_chart(victims_chart, use_container_width=True)
    
    fatalities_chart = create_area_chart(
        trends_df, 
        'Year', 
        'Fatalities', 
        'Child Fatalities Over Time',
        '#e74c3c'
    )
    st.altair_chart(fatalities_chart, use_container_width=True)
    
    # Key terms and definitions
    st.markdown("## Key Terms")
    with st.expander("What is child maltreatment?"):
        st.markdown("""
        Child maltreatment includes all types of abuse and neglect of a child under the age of 18 by a parent, caregiver, or another person in a custodial role.
        
        The four common types of maltreatment include:
        - **Physical abuse**: Physical acts that caused or could have caused physical injury
        - **Sexual abuse**: Involving a child in sexual acts
        - **Emotional abuse**: Behaviors that harm a child's self-worth or emotional well-being
        - **Neglect**: Failure to provide for a child's basic needs
        """)
    
    with st.expander("How is the victimization rate calculated?"):
        st.markdown("""
        The victimization rate is calculated as the number of victims per 1,000 children in the population.
        
        For example, a victimization rate of 8.9 means that 8.9 out of every 1,000 children in the population were determined to be victims of maltreatment.
        """)
    
    with st.expander("What is counted in the data?"):
        st.markdown("""
        The data primarily includes cases that were:
        1. Reported to child protective services
        2. Screened in for investigation or assessment
        3. Received a disposition (finding)
        
        It's important to note that these statistics likely underestimate the true prevalence of child maltreatment, as many cases go unreported.
        """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")