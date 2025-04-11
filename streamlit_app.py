import streamlit as st
import pandas as pd
import altair as alt
import time
from utils.helpers import load_css

# This must be the first Streamlit command!
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
load_css()

# -------------------------------
# Home Page
# -------------------------------
st.title("Child Maltreatment Data Dashboard")

# Introduction with brief overview and mission statement
st.markdown("""
## Behind Every Number is a Story

Welcome to this interactive dashboard that presents insights about child maltreatment in the United States. 
This dashboard is designed to not only show the data but to tell the story behind the numbers.

**What you'll find:**
- A narrative that explains the human impact of child maltreatment
- National trends with interactive visualizations
- State-level explorer with mapping capabilities
- Demographic disparities analysis
- Survivor stories that put faces to the statistics
- Interactive quiz to test your knowledge
- Resource hub for support and prevention initiatives

Use the sidebar navigation to explore each section.
""")

# Add a compelling image 
st.image(
    "https://www.kvc.org/wp-content/uploads/2023/04/child-abuse-prevention-month-poster-april-vector.jpg_s1024x1024wisk20cU4Ji6zCkryXI-2I7Ri0dHLJNKY4Ma2nMuaXp0p4XvvU-1024x576.jpg",
    use_container_width=True,
    caption="Child abuse prevention awareness"
)

# Add a "Call to Action" section
st.markdown("""
## Our Mission

This dashboard aims to raise awareness about child maltreatment by:
1. Making complex data accessible and understandable
2. Highlighting both progress and ongoing challenges
3. Centering the human experience in data analysis
4. Supporting evidence-based prevention efforts

**Who is this for?**
- Professionals who need data to inform policy and practice
- Community members who want to understand and support change
- Students and researchers studying child welfare
- Anyone interested in child protection and well-being
""")

# Preview key statistic with animation
st.subheader("A Glimpse at the Data")
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Children affected by maltreatment annually",
            value="~600,000",
            delta="-15% since 2018"
        )
        st.caption("Source: Aggregated data from HHS Child Maltreatment reports")
    
    with col2:
        st.metric(
            label="Child fatalities due to abuse/neglect",
            value="~1,800",
            delta="+17% since 2018",
            delta_color="inverse"
        )
        st.caption("Source: Aggregated data from HHS Child Maltreatment reports")

# Progress bar to encourage exploration
st.subheader("Ready to explore the full dashboard?")
st.write("Start your journey through the data")
progress_bar = st.progress(0)
for percent in range(0, 101, 10):
    progress_bar.progress(percent)
    time.sleep(0.05)  # animation delay to simulate progress

st.success("Please use the sidebar to navigate through the different sections!")

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")