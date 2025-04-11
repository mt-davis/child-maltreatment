import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, display_fact_box, create_comparison_bar
from utils.charts import create_interactive_map, create_bar_chart, create_choropleth_map, create_pie_chart
from data.data_loader import get_state_data

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - State Explorer",
    page_icon="🗺️",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("State Explorer")
st.markdown("""
Explore child maltreatment statistics by state to understand regional variations and patterns.
Use the interactive map and state selector to dive into specific state data.
""")

# Load state data
state_df = get_state_data()

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Interactive Map", "State Comparison", "State Details"])

with tab1:
    st.markdown("## Interactive U.S. Map of Child Maltreatment Statistics")
    st.markdown("Click on any state marker to see detailed information.")
    
    # Create the interactive map
    map_metric = st.radio(
        "Select map visualization metric:",
        ["Victim Count", "Victim Rate", "Fatalities"],
        horizontal=True,
        key="map_metric"
    )
    
    if map_metric == "Victim Count":
        popup_cols = ["Victims", "Victim_Rate", "Fatalities"]
        map_title = "Child Maltreatment Victims by State"
    elif map_metric == "Victim Rate":
        popup_cols = ["Victim_Rate", "Victims", "Fatalities"]
        map_title = "Child Maltreatment Rate per 1,000 Children by State"
    else:
        popup_cols = ["Fatalities", "Victims", "Victim_Rate"]
        map_title = "Child Maltreatment Fatalities by State"
    
    # Create the map
    m = create_interactive_map(
        state_df,
        "Latitude",
        "Longitude",
        popup_cols,
        map_title,
        zoom_start=4
    )
    
    # Display the map
    st_folium(m, width=1000, height=500)
    
    st.markdown("""
    **Note:** The map displays the locations of state capitals or major cities as proxies for state locations.
    Click on the markers to see specific state statistics.
    """)

with tab2:
    st.markdown("## State Comparison")
    
    # Let user select states to compare
    states_to_compare = st.multiselect(
        "Select states to compare:",
        sorted(state_df["State"].unique()),
        default=["California", "Texas", "New York", "Florida", "Illinois"]
    )
    
    if states_to_compare:
        # Filter data for selected states
        comparison_df = state_df[state_df["State"].isin(states_to_compare)]
        
        # Metric to compare
        compare_metric = st.radio(
            "Select metric to compare:",
            ["Victims", "Victim_Rate", "Fatalities"],
            horizontal=True,
            key="compare_metric"
        )
        
        # Create comparison chart
        if compare_metric == "Victims":
            title = "Total Child Maltreatment Victims by State"
            color = "#3498db"
        elif compare_metric == "Victim_Rate":
            title = "Child Maltreatment Rate per 1,000 Children by State"
            color = "#2ecc71"
        else:
            title = "Child Fatalities Due to Maltreatment by State"
            color = "#e74c3c"
        
        comparison_chart = create_bar_chart(
            comparison_df,
            "State",
            compare_metric,
            title,
            color=color
        )
        
        st.altair_chart(comparison_chart, use_container_width=True)
        
        # Add a data table below
        st.markdown("### Detailed Comparison")
        st.dataframe(
            comparison_df.sort_values(by=compare_metric, ascending=False)[
                ["State", "Victims", "Victim_Rate", "Fatalities"]
            ].reset_index(drop=True),
            use_container_width=True
        )
        
        # Show type breakdown comparison
        st.markdown("### Maltreatment Type Comparison")
        
        # Create a new dataframe with the type breakdown
        types_comparison = pd.DataFrame()
        for state in states_to_compare:
            state_row = state_df[state_df["State"] == state].iloc[0]
            types_comparison = types_comparison.append({
                "State": state,
                "Neglect": state_row["Neglect_Percent"],
                "Physical": state_row["Physical_Percent"],
                "Sexual": state_row["Sexual_Percent"],
                "Other": 100 - (state_row["Neglect_Percent"] + state_row["Physical_Percent"] + state_row["Sexual_Percent"])
            }, ignore_index=True)
        
        # Melt for easier charting
        melted_types = pd.melt(
            types_comparison, 
            id_vars=["State"], 
            value_vars=["Neglect", "Physical", "Sexual", "Other"],
            var_name="Type", 
            value_name="Percentage"
        )
        
        # Create stacked bar chart
        type_chart = alt.Chart(melted_types).mark_bar().encode(
            x=alt.X("State:N", title="State"),
            y=alt.Y("Percentage:Q", title="Percentage", stack="normalize"),
            color=alt.Color(
                "Type:N", 
                scale=alt.Scale(
                    domain=["Neglect", "Physical", "Sexual", "Other"],
                    range=["#3498db", "#e74c3c", "#9b59b6", "#95a5a6"]
                )
            ),
            tooltip=["State", "Type", "Percentage"]
        ).properties(
            title="Maltreatment Types by State (%)"
        ).interactive()
        
        st.altair_chart(type_chart, use_container_width=True)
    else:
        st.info("Please select at least one state to compare.")

with tab3:
    st.markdown("## State Details")
    
    # State selector
    selected_state = st.selectbox(
        "Select a state:",
        sorted(state_df["State"].unique())
    )
    
    # Get the data for the selected state
    state_info = state_df[state_df["State"] == selected_state].iloc[0]
    
    # Create a two-column layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"### {selected_state} Statistics")
        
        # Key metrics
        st.markdown(f"""
        <div class="metric-card">
            <h3>Child Victims</h3>
            <div class="metric-value">{int(state_info['Victims']):,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Victimization Rate</h3>
            <div class="metric-value">{state_info['Victim_Rate']}</div>
            <div class="metric-description">per 1,000 children</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Child Fatalities</h3>
            <div class="metric-value">{int(state_info['Fatalities']):,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Compare to national averages
        st.markdown("### Comparison to National Averages")
        
        # Calculate national averages
        nat_avg_victims = state_df["Victims"].mean()
        nat_avg_rate = state_df["Victim_Rate"].mean()
        nat_avg_fatalities = state_df["Fatalities"].mean()
        
        # Create comparison bars
        st.markdown("#### Victims")
        create_comparison_bar(
            int(state_info["Victims"]), 
            int(state_df["Victims"].max()), 
            selected_state
        )
        create_comparison_bar(
            int(nat_avg_victims), 
            int(state_df["Victims"].max()), 
            "National Average"
        )
        
        st.markdown("#### Victimization Rate")
        create_comparison_bar(
            state_info["Victim_Rate"], 
            state_df["Victim_Rate"].max(), 
            selected_state
        )
        create_comparison_bar(
            nat_avg_rate, 
            state_df["Victim_Rate"].max(), 
            "National Average"
        )
        
        st.markdown("#### Fatalities")
        create_comparison_bar(
            int(state_info["Fatalities"]), 
            int(state_df["Fatalities"].max()), 
            selected_state
        )
        create_comparison_bar(
            int(nat_avg_fatalities), 
            int(state_df["Fatalities"].max()), 
            "National Average"
        )
    
    with col2:
        st.markdown("### Maltreatment Type Breakdown")
        
        # Create data for pie chart
        type_data = pd.DataFrame({
            "Type": ["Neglect", "Physical Abuse", "Sexual Abuse", "Other"],
            "Percentage": [
                state_info["Neglect_Percent"],
                state_info["Physical_Percent"],
                state_info["Sexual_Percent"],
                100 - (state_info["Neglect_Percent"] + state_info["Physical_Percent"] + state_info["Sexual_Percent"])
            ]
        })
        
        # Create pie chart
        fig = create_pie_chart(
            type_data,
            "Type",
            "Percentage",
            f"Maltreatment Types in {selected_state}"
        )
        
        st.pyplot(fig)
        
        # Regional information and context
        st.markdown("### Regional Context")
        
        # Find neighboring states (simplified for this example)
        # In a real app, you would have actual geographic data for this
        all_states = sorted(state_df["State"].unique())
        nearby_states = []
        
        # This is a simplified example - in a real app, you would determine actual neighboring states
        for i, state in enumerate(all_states):
            if state == selected_state:
                # Get a few surrounding states as "neighbors"
                start_idx = max(0, i - 2)
                end_idx = min(len(all_states), i + 3)
                nearby_states = [s for s in all_states[start_idx:end_idx] if s != selected_state]
                break
        
        if nearby_states:
            st.markdown(f"#### How {selected_state} compares to nearby states:")
            
            # Create a regional comparison dataframe
            region_df = state_df[state_df["State"].isin([selected_state] + nearby_states)]
            
            # Create bar chart for regional comparison
            regional_chart = alt.Chart(region_df).mark_bar().encode(
                x=alt.X("Victim_Rate:Q", title="Victimization Rate"),
                y=alt.Y("State:N", title=None, sort="-x"),
                color=alt.condition(
                    alt.datum.State == selected_state,
                    alt.value("#3498db"),
                    alt.value("#95a5a6")
                ),
                tooltip=["State", "Victim_Rate", "Victims", "Fatalities"]
            ).properties(
                title=f"Victimization Rate: {selected_state} vs. Nearby States"
            ).interactive()
            
            st.altair_chart(regional_chart, use_container_width=True)

# State rankings section
st.markdown("## State Rankings")

# Metric for ranking
rank_metric = st.radio(
    "Select ranking metric:",
    ["Victim_Rate", "Victims", "Fatalities"],
    horizontal=True,
    key="rank_metric"
)

# Number of states to show
top_n = st.slider("Number of states to display:", 5, 15, 10)

# Sort the dataframe
if rank_metric == "Victim_Rate":
    title = "States with Highest Maltreatment Rates"
    color = "#2ecc71"
elif rank_metric == "Victims":
    title = "States with Most Child Maltreatment Victims"
    color = "#3498db"
else:
    title = "States with Most Child Fatalities"
    color = "#e74c3c"

# Create ranking dataframe
ranking_df = state_df.sort_values(by=rank_metric, ascending=False).head(top_n)

# Create the chart
ranking_chart = create_bar_chart(
    ranking_df,
    "State",
    rank_metric,
    title,
    color=color
)

st.altair_chart(ranking_chart, use_container_width=True)

# Data sources and methodology
with st.expander("Data Sources & Methodology"):
    st.markdown("""
    ### Data Sources
    
    The state-level data presented in this dashboard is aggregated from several sources:
    
    - **Primary Source**: U.S. Department of Health & Human Services, Administration for Children and Families, Children's Bureau annual state data tables
    - State-level child welfare agencies and their annual reports
    - National Child Abuse and Neglect Data System (NCANDS)
    
    ### Methodology Notes
    
    - **State Variations**: States may vary in how they define and categorize maltreatment, which affects comparability
    - **Reporting Differences**: States may have different reporting requirements and systems, which can impact their statistics
    - **Population Adjustments**: Victimization rates are calculated per 1,000 children to account for different state populations
    - **Limitations**: These figures likely underestimate the true prevalence of child maltreatment
    
    For more detailed methodology information, please refer to the original reports.
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")