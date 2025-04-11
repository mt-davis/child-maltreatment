import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, display_fact_box, animate_stat_reveal, create_impact_visualization
from utils.charts import create_line_chart, create_multi_line_chart, create_area_chart, create_stacked_area_chart
from data.data_loader import get_national_trends

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - National Trends",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("National Trends Over Time")
st.markdown("""
This dashboard presents national trends in child maltreatment over the past decade.
Explore how various metrics have changed over time, and what these changes mean for child welfare.
""")

# Load data
trends_df = get_national_trends()

# Summary metrics for the most recent year
latest_year = trends_df["Year"].max()
latest_data = trends_df[trends_df["Year"] == latest_year].iloc[0]
earliest_year = trends_df["Year"].min()
earliest_data = trends_df[trends_df["Year"] == earliest_year].iloc[0]

# Calculate percent changes
victim_change = ((latest_data["Victims"] - earliest_data["Victims"]) / earliest_data["Victims"]) * 100
fatality_change = ((latest_data["Fatalities"] - earliest_data["Fatalities"]) / earliest_data["Fatalities"]) * 100
rate_change = ((latest_data["Victim_Rate"] - earliest_data["Victim_Rate"]) / earliest_data["Victim_Rate"]) * 100

# Dashboard layout
st.markdown("## Key Metrics at a Glance")

# Create 3 columns for the key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>Child Victims</h3>
        <div class="metric-value">{:,}</div>
        <div class="metric-description">
            <span style="color: {}; font-weight: bold;">{:.1f}%</span> {} since {}
        </div>
    </div>
    """.format(
        int(latest_data["Victims"]),
        "#e74c3c" if victim_change >= 0 else "#2ecc71",
        abs(victim_change),
        "increase" if victim_change >= 0 else "decrease",
        earliest_year
    ), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Child Fatalities</h3>
        <div class="metric-value">{:,}</div>
        <div class="metric-description">
            <span style="color: {}; font-weight: bold;">{:.1f}%</span> {} since {}
        </div>
    </div>
    """.format(
        int(latest_data["Fatalities"]),
        "#e74c3c" if fatality_change >= 0 else "#2ecc71",
        abs(fatality_change),
        "increase" if fatality_change >= 0 else "decrease",
        earliest_year
    ), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Victimization Rate</h3>
        <div class="metric-value">{:.1f}</div>
        <div class="metric-description">
            per 1,000 children
            <br>
            <span style="color: {}; font-weight: bold;">{:.1f}%</span> {} since {}
        </div>
    </div>
    """.format(
        latest_data["Victim_Rate"],
        "#e74c3c" if rate_change >= 0 else "#2ecc71",
        abs(rate_change),
        "increase" if rate_change >= 0 else "decrease",
        earliest_year
    ), unsafe_allow_html=True)

# Impact visualization
create_impact_visualization(
    int(latest_data["Victims"]), 
    icon="👧👦", 
    title="Children Affected Annually", 
    description="children were victims of maltreatment in the most recent reporting year"
)

# Victims trend chart
st.markdown("## Trends in Reported Victims")

# Options for customization
chart_type = st.radio(
    "Select chart type:",
    ["Line Chart", "Area Chart"],
    horizontal=True,
    key="victims_chart_type"
)

if chart_type == "Line Chart":
    victims_chart = create_line_chart(
        trends_df,
        "Year",
        "Victims",
        "Number of Child Maltreatment Victims Over Time"
    )
else:
    victims_chart = create_area_chart(
        trends_df,
        "Year",
        "Victims",
        "Number of Child Maltreatment Victims Over Time"
    )

st.altair_chart(victims_chart, use_container_width=True)

# Add context to the chart
st.markdown("""
The number of reported victims has shown a general decline over the past decade. This could be due to:
- Improved prevention efforts
- Changes in reporting practices
- Variations in state definitions of maltreatment
- Policy changes affecting how cases are classified

**Note:** These figures represent cases that were reported and substantiated by child protective services. Many cases go unreported.
""")

# Create tabs for exploring different metrics
st.markdown("## Additional Trend Analyses")
tab1, tab2, tab3 = st.tabs(["Child Fatalities", "Victimization Rates", "Maltreatment Types"])

with tab1:
    st.markdown("### Trends in Child Fatalities")
    fatalities_chart = create_line_chart(
        trends_df,
        "Year",
        "Fatalities",
        "Number of Child Fatalities Due to Maltreatment",
        color="#e74c3c"
    )
    st.altair_chart(fatalities_chart, use_container_width=True)
    
    st.markdown("""
    While overall victimization has decreased, fatalities have shown an upward trend. This concerning pattern suggests:
    - Potential increases in severe abuse cases
    - Improvements in identifying and classifying maltreatment-related deaths
    - Continued gaps in protecting the most vulnerable children
    """)
    
    # Display fact box
    display_fact_box(
        "Most Vulnerable Age Group", 
        "Children under 1 year of age account for nearly 50% of all fatalities. Their vulnerability and dependency make them particularly at risk."
    )

with tab2:
    st.markdown("### Victimization Rate Trends")
    rate_chart = create_line_chart(
        trends_df,
        "Year",
        "Victim_Rate",
        "Victimization Rate per 1,000 Children",
        color="#2ecc71"
    )
    st.altair_chart(rate_chart, use_container_width=True)
    
    st.markdown("""
    The victimization rate provides a standardized measure that accounts for changes in the child population over time.
    
    A declining rate suggests real progress in reducing child maltreatment relative to the population, though significant work remains.
    """)

with tab3:
    st.markdown("### Maltreatment Types Over Time")
    
    # Create a dataframe for maltreatment types
    types_df = trends_df[["Year", "Neglect_Percent", "Physical_Abuse_Percent", "Sexual_Abuse_Percent"]].copy()
    
    # Calculate "Other" category
    types_df["Other_Percent"] = 100 - (types_df["Neglect_Percent"] + types_df["Physical_Abuse_Percent"] + types_df["Sexual_Abuse_Percent"])
    
    # Melt the dataframe for easier charting
    melted_df = pd.melt(
        types_df, 
        id_vars=["Year"], 
        value_vars=["Neglect_Percent", "Physical_Abuse_Percent", "Sexual_Abuse_Percent", "Other_Percent"],
        var_name="Maltreatment_Type", 
        value_name="Percentage"
    )
    
    # Clean up type names for display
    melted_df["Maltreatment_Type"] = melted_df["Maltreatment_Type"].str.replace("_Percent", "")
    
    # Create stacked area chart
    stacked_chart = alt.Chart(melted_df).mark_area().encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Percentage:Q", title="Percentage", stack="normalize"),
        color=alt.Color(
            "Maltreatment_Type:N", 
            scale=alt.Scale(
                domain=["Neglect", "Physical_Abuse", "Sexual_Abuse", "Other"],
                range=["#3498db", "#e74c3c", "#9b59b6", "#95a5a6"]
            ),
            legend=alt.Legend(title="Maltreatment Type")
        ),
        tooltip=["Year", "Maltreatment_Type", "Percentage"]
    ).properties(
        title="Maltreatment Types as Percentage of Cases"
    ).interactive()
    
    st.altair_chart(stacked_chart, use_container_width=True)
    
    st.markdown("""
    Neglect consistently accounts for the majority of child maltreatment cases, followed by physical abuse and sexual abuse.
    
    This breakdown has remained relatively stable over time, highlighting the ongoing need for:
    - Family support services that address basic needs
    - Parenting education and resources
    - Prevention of all forms of maltreatment
    """)

# Interactive exploration section
st.markdown("## Interactive Exploration")
st.markdown("Compare multiple metrics over time to understand relationships between different aspects of child maltreatment.")

# Let users select which metrics to compare
metrics_to_compare = st.multiselect(
    "Select metrics to compare:",
    ["Victims", "Fatalities", "Victim_Rate"],
    default=["Victims", "Fatalities"]
)

if metrics_to_compare:
    multi_metric_chart = create_multi_line_chart(
        trends_df,
        "Year",
        metrics_to_compare,
        "Comparison of Selected Metrics Over Time"
    )
    st.altair_chart(multi_metric_chart, use_container_width=True)

# Data sources and methodology
with st.expander("Data Sources & Methodology"):
    st.markdown("""
    ### Data Sources
    
    The data presented in this dashboard is aggregated from several sources:
    
    - **Primary Source**: U.S. Department of Health & Human Services, Administration for Children and Families, Children's Bureau Child Maltreatment Reports
    - Annual reports from the National Child Abuse and Neglect Data System (NCANDS)
    - State-level child welfare agencies
    
    ### Methodology Notes
    
    - **Definitions**: States may vary in how they define and categorize maltreatment
    - **Reporting**: Data includes only cases reported to and confirmed by child protective services
    - **Limitations**: These figures likely underestimate the true prevalence of child maltreatment
    
    For more detailed methodology information, please refer to the original reports.
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")