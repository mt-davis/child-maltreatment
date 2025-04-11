import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium

# ------------------------------
# Inline Data Definitions
# ------------------------------

@st.cache(show_spinner=False)
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

@st.cache(show_spinner=False)
def get_national_trends():
    data = {
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Victims": [678000, 660000, 650000, 640000, 558899],
        "Fatalities": [1700, 1750, 1800, 1850, 1990]
    }
    return pd.DataFrame(data)

@st.cache(show_spinner=False)
def get_disparities_data():
    data = {
        "Race": ["American Indian/Alaska Native", "African American", "White", "Hispanic", "Asian"],
        "Victim_Rate": [14.3, 12.1, 6.0, 6.5, 4.0]
    }
    return pd.DataFrame(data)

@st.cache(show_spinner=False)
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
        }
    ]

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select a section",
    ["Home", "Trends Dashboard", "State Explorer", "Disparities", "Survivor Voices", "Quiz", "Resource Hub"]
)

# ------------------------------
# Home Page
# ------------------------------
if page == "Home":
    st.title("Child Maltreatment Data Dashboard")
    st.markdown("""
    Welcome to this interactive dashboard that presents insights about child maltreatment in the United States.
    
    The app covers **national trends**, **state-level data**, **disparities by demographics**, **case outcomes**, and **prevention efforts**.  
    Explore interactive maps, charts, survivor voices, and even test your knowledge with a short quiz.
    """)
    st.image("https://via.placeholder.com/800x300.png?text=Child+Maltreatment+Awareness", use_column_width=True)

# ------------------------------
# National Trends Dashboard
# ------------------------------
elif page == "Trends Dashboard":
    st.title("National Trends Over Time")
    trends_df = get_national_trends()
    
    st.markdown("### Trends in Reported Victims")
    line_chart = alt.Chart(trends_df).mark_line(point=True).encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Victims:Q", title="Number of Victims"),
        tooltip=["Year", "Victims"]
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)
    
    st.markdown("### Trends in Child Fatalities")
    fatality_chart = alt.Chart(trends_df).mark_line(point=True, color='red').encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Fatalities:Q", title="Number of Fatalities"),
        tooltip=["Year", "Fatalities"]
    ).interactive()
    st.altair_chart(fatality_chart, use_container_width=True)
    
    st.markdown("""
    **Data Sources:**  
    Data is aggregated from the HHS Child Maltreatment reports and related datasets.
    """)

# ------------------------------
# State Explorer with Interactive Map
# ------------------------------
elif page == "State Explorer":
    st.title("State Explorer")
    state_df = get_state_data()
    
    # Sidebar state filter specific for state explorer
    state_selected = st.sidebar.selectbox("Select a State", sorted(state_df["State"].unique()))
    st.markdown(f"### Data for **{state_selected}**")
    state_info = state_df[state_df["State"] == state_selected]
    st.write(state_info)
    
    st.markdown("### Interactive U.S. Map of Child Maltreatment Statistics")
    # Initialize folium map centered in the US
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add markers for each state
    for idx, row in state_df.iterrows():
        lat = row["Latitude"]
        lon = row["Longitude"]
        popup_text = f"<strong>{row['State']}</strong><br>Victims: {row['Victims']}<br>Rate: {row['Victim_Rate']} per 1,000<br>Fatalities: {row['Fatalities']}"
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
    
    # Render the folium map in Streamlit
    st_data = st_folium(m, width=700)
    
    st.markdown("""
    **Data Sources:**  
    The state-level data are based on aggregated child maltreatment reports.
    """)

# ------------------------------
# Disparities Dashboard
# ------------------------------
elif page == "Disparities":
    st.title("Disparities in Child Maltreatment")
    disparity_df = get_disparities_data()
    
    st.markdown("### Victimization Rate by Race/Ethnicity")
    bar_chart = alt.Chart(disparity_df).mark_bar().encode(
        x=alt.X("Race:N", title="Race/Ethnicity"),
        y=alt.Y("Victim_Rate:Q", title="Victimization Rate per 1,000"),
        tooltip=["Race", "Victim_Rate"]
    )
    st.altair_chart(bar_chart, use_container_width=True)
    
    st.markdown("""
    The chart highlights disparities with marginalized communities experiencing higher victim rates.
    """)
    
    st.markdown("""
    **Data Source:**  
    Disparity data summarized from federal statistics and research reports.
    """)

# ------------------------------
# Survivor Voices
# ------------------------------
elif page == "Survivor Voices":
    st.title("Survivor Voices")
    quotes = get_quotes()
    
    st.markdown("### Hear from Survivors")
    for quote in quotes:
        st.info(f"“{quote['quote']}” — *{quote['name']}*")
    
    st.markdown("""
    **Note:** Survivor narratives are shared with permission and are intended to illustrate the human impact.
    """)

# ------------------------------
# Quiz Section
# ------------------------------
elif page == "Quiz":
    st.title("Child Maltreatment Quiz")
    st.markdown("Test your knowledge on child maltreatment with the questions below.")
    
    st.markdown("**Question 1:** Neglect is the most common form of child maltreatment. True or False?")
    answer = st.radio("Your Answer", options=["True", "False"], key="q1")
    if st.button("Submit Answer", key="btn1"):
        if answer == "True":
            st.success("Correct! Neglect accounts for approximately 74% of cases.")
        else:
            st.error("Incorrect. The correct answer is True.")
    
    st.markdown("**Question 2:** Which age group has the highest victimization rate in the U.S.?")
    answer2 = st.radio("Your Answer", options=["Infants under 1", "Teenagers", "School-aged children"], key="q2")
    if st.button("Submit Answer", key="btn2"):
        if answer2 == "Infants under 1":
            st.success("Correct! Babies under 1 have the highest victimization rate.")
        else:
            st.error("Incorrect. The correct answer is 'Infants under 1'.")
    
    st.markdown("**Question 3:** Which group typically faces the highest rates of maltreatment?")
    answer3 = st.radio("Your Answer", options=["White children", "American Indian/Alaska Native children", "Asian children"], key="q3")
    if st.button("Submit Answer", key="btn3"):
        if answer3 == "American Indian/Alaska Native children":
            st.success("Correct! Data indicate that American Indian/Alaska Native children have some of the highest victimization rates.")
        else:
            st.error("Incorrect. The correct answer is 'American Indian/Alaska Native children'.")
    
    st.markdown("""
    **Data Sources:**  
    Quiz questions are based on data from federal reports on child maltreatment.
    """)

# ------------------------------
# Resource Hub
# ------------------------------
elif page == "Resource Hub":
    st.title("Resource Hub")
    st.markdown("### Explore Prevention Programs, Policies, and Support Resources")
    
    resources = {
        "Child Abuse Prevention and Treatment Act (CAPTA)": "https://www.childwelfare.gov/topics/systemwide/laws-policies/statutes/capta/",
        "Family First Prevention Services Act": "https://www.acf.hhs.gov/cb/resource/family-first-prevention-services-act-ffpsa",
        "Zero Abuse Project": "https://zeroabuse.org/",
        "National Children’s Alliance": "https://www.nationalchildrensalliance.org/",
        "Prevent Child Abuse America": "https://preventchildabuse.org/"
    }
    
    search_query = st.text_input("Search Resources")
    if search_query:
        filtered = {name: link for name, link in resources.items() if search_query.lower() in name.lower()}
    else:
        filtered = resources
    
    for name, link in filtered.items():
        st.markdown(f"- [{name}]({link})")
    
    st.markdown("""
    **Additional Resources:**  
    For more detailed publications and support, please visit the links above.
    """)

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")
