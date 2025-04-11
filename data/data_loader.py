import streamlit as st
import pandas as pd
import json

# Cache all data loading functions to improve performance
@st.cache_data(show_spinner=False)
def get_state_data():
    """
    Load state-level child maltreatment data.
    In a real app, this would load from a CSV or API.
    """
    data = {
        "State": ["Massachusetts", "Mississippi", "New Jersey", "California", "Texas",
                  "Florida", "New York", "Illinois", "Ohio", "Michigan", "Washington",
                  "Oregon", "Colorado", "Arizona", "Georgia", "Pennsylvania", "Virginia",
                  "North Carolina", "Tennessee", "Minnesota", "Wisconsin", "Louisiana",
                  "Alabama", "Kentucky", "Indiana", "Missouri", "Oklahoma", "Maryland",
                  "Connecticut", "Iowa", "Nebraska", "New Mexico", "Utah", "Nevada"],
        "Victims": [20000, 15000, 18000, 80000, 75000,
                    65000, 70000, 50000, 40000, 35000,
                    22000, 19000, 21000, 38000, 45000,
                    32000, 28000, 30000, 25000, 18000,
                    16000, 24000, 23000, 21000, 26000,
                    22000, 19000, 17000, 12000, 14000,
                    9000, 11000, 10000, 14000],
        "Victim_Rate": [16.5, 12.0, 1.6, 8.0, 9.2,
                        10.1, 11.3, 7.5, 6.8, 5.5,
                        9.8, 8.2, 7.1, 8.6, 9.4,
                        7.9, 6.3, 7.8, 8.4, 5.2,
                        4.9, 10.5, 10.2, 9.5, 8.7,
                        7.6, 9.3, 6.2, 5.8, 6.9,
                        7.0, 9.1, 6.7, 7.3],
        "Fatalities": [300, 400, 150, 600, 500,
                       550, 500, 350, 300, 250,
                       180, 160, 170, 280, 330,
                       250, 220, 240, 210, 130,
                       120, 200, 190, 170, 210,
                       180, 170, 130, 90, 110,
                       70, 90, 80, 110],
        "Neglect_Percent": [78, 68, 72, 74, 71,
                            73, 75, 70, 69, 72,
                            71, 73, 69, 70, 74,
                            75, 73, 71, 72, 68,
                            67, 74, 73, 71, 72,
                            68, 73, 70, 71, 69,
                            72, 70, 69, 73],
        "Physical_Percent": [15, 20, 16, 14, 19,
                             16, 13, 18, 19, 17,
                             17, 15, 18, 19, 16,
                             15, 17, 18, 17, 20,
                             21, 15, 17, 18, 17,
                             20, 17, 18, 19, 20,
                             17, 19, 20, 17],                    
        "Sexual_Percent": [7, 12, 12, 12, 10,
                           11, 12, 12, 12, 11,
                           12, 12, 13, 11, 10,
                           10, 10, 11, 11, 12,
                           12, 11, 10, 11, 11,
                           12, 10, 12, 10, 11,
                           11, 11, 11, 10],
        "Latitude": [42.4072, 32.3547, 40.0583, 36.7783, 31.9686,
                     27.6648, 43.2994, 40.6331, 40.4173, 44.3148,
                     47.7511, 44.1419, 39.5501, 34.0489, 33.0406,
                     40.5908, 37.4316, 35.7596, 35.5175, 46.7296,
                     44.2563, 31.1695, 32.3182, 37.6681, 39.7684,
                     38.5767, 35.4676, 39.0458, 41.6032, 41.8780,
                     41.4925, 34.5199, 39.3210, 38.8026],
        "Longitude": [-71.3824, -89.3985, -74.4057, -119.4179, -99.9018,
                      -81.5158, -74.2179, -89.3985, -82.9071, -85.6024,
                      -120.7401, -120.5381, -105.7821, -111.0937, -83.6431,
                      -77.0200, -78.6569, -79.0193, -86.5804, -94.6859,
                      -89.6385, -91.8816, -86.9023, -84.6701, -86.1581,
                      -92.1735, -97.5164, -76.6413, -72.7559, -93.0977,
                      -99.9018, -105.8701, -111.0937, -116.4194]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_national_trends():
    """
    Load national trend data for child maltreatment.
    In a real app, this would load from a CSV or API.
    """
    data = {
        "Year": list(range(2013, 2023)),
        "Victims": [678000, 670000, 665000, 662000, 660000, 
                    650000, 640000, 620000, 590000, 558899],
        "Fatalities": [1520, 1560, 1580, 1650, 1700, 
                      1750, 1800, 1850, 1920, 1990],
        "Victim_Rate": [9.1, 9.0, 8.9, 8.8, 8.7, 
                        8.6, 8.5, 8.3, 8.0, 7.7],
        "Neglect_Percent": [75.0, 75.3, 75.3, 74.8, 74.9, 
                           75.1, 75.5, 75.9, 76.1, 76.3],
        "Physical_Abuse_Percent": [17.0, 16.8, 16.7, 17.2, 17.5, 
                                  17.2, 17.5, 17.0, 16.9, 16.7],
        "Sexual_Abuse_Percent": [8.3, 8.3, 8.4, 8.5, 8.6, 
                                8.5, 8.2, 9.2, 9.3, 9.5]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_disparities_data():
    """
    Load data on disparities in child maltreatment.
    In a real app, this would load from a CSV or API.
    """
    data = {
        "Race": ["American Indian/Alaska Native", "African American", "Multiple Race", 
                 "White", "Hispanic", "Native Hawaiian/Pacific Islander", "Asian"],
        "Victim_Rate": [14.3, 12.1, 10.2, 6.0, 6.5, 5.7, 4.0],
        "Percent_Of_Population": [0.9, 13.8, 2.7, 51.5, 25.3, 0.3, 5.5]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_age_data():
    """
    Load data on child maltreatment by age group.
    In a real app, this would load from a CSV or API.
    """
    data = {
        "Age_Group": ["<1 year", "1-3 years", "4-7 years", "8-11 years", "12-15 years", "16-17 years"],
        "Victim_Rate": [24.5, 11.8, 9.2, 7.5, 6.7, 5.1]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_perpetrator_data():
    """
    Load data on perpetrator relationships.
    In a real app, this would load from a CSV or API.
    """
    data = {
        "Relationship": ["Parents", "Relatives", "Partner of Parent", "Other", "Unknown/Missing"],
        "Percentage": [77.5, 7.2, 6.3, 6.0, 3.0]
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def get_quotes():
    """
    Load survivor quotes.
    In a real app, this would load from a database or API.
    """
    return [
        {
            "quote": "I would write letters to my third-grade teacher. I never had the courage to send them, but I always held out hope that someday she would notice. I just wished so often that she would save me.",
            "name": "Tiffani Shurtleff",
            "age": "34",
            "background": "Experienced neglect and emotional abuse throughout childhood"
        },
        {
            "quote": "My childhood was filled with physical abuse from the person who was supposed to love me; sexual abuse from people who were supposed to protect me… I just wanted someone to save me. I needed help. I needed to be rescued.",
            "name": "Kristina",
            "age": "29",
            "background": "Survivor of multiple forms of abuse"
        },
        {
            "quote": "I remember feeling so isolated. The trauma wasn't just what happened, but that I had no one to tell. School was my safe place, and looking back, I wish a teacher had seen the signs.",
            "name": "Michael",
            "age": "41",
            "background": "Experienced physical abuse from age 6 to 14"
        },
        {
            "quote": "Prevention is everything. If someone had intervened, if our family had gotten support, my story could have been different. Now I work to change the story for other children.",
            "name": "Sarah",
            "age": "37",
            "background": "Experienced neglect due to parental substance abuse"
        },
        {
            "quote": "What saved me was one adult who believed me and took action. One person can make all the difference in a child's life.",
            "name": "James",
            "age": "28",
            "background": "Survivor who now works as a child advocate"
        }
    ]

@st.cache_data(show_spinner=False)
def get_resources():
    """
    Load resource information.
    In a real app, this would load from a database or API.
    """
    return {
        "Prevention Programs": [
            {
                "name": "Safe Care",
                "description": "Evidence-based home visitation program designed to prevent child maltreatment",
                "url": "https://safecarecmh.org/",
                "type": "Prevention"
            },
            {
                "name": "Triple P Positive Parenting Program",
                "description": "Multi-level system of parenting and family support",
                "url": "https://www.triplep.net/",
                "type": "Prevention"
            },
            {
                "name": "Nurse-Family Partnership",
                "description": "Evidence-based community health program for first-time moms",
                "url": "https://www.nursefamilypartnership.org/",
                "type": "Prevention"
            }
        ],
        "Policies & Legislation": [
            {
                "name": "Child Abuse Prevention and Treatment Act (CAPTA)",
                "description": "Federal legislation providing funding to states in support of prevention, assessment, investigation, and treatment",
                "url": "https://www.childwelfare.gov/topics/systemwide/laws-policies/statutes/capta/",
                "type": "Policy"
            },
            {
                "name": "Family First Prevention Services Act",
                "description": "Law that restructures federal child welfare funding to support families and prevent foster care placement",
                "url": "https://www.acf.hhs.gov/cb/resource/family-first-prevention-services-act-ffpsa",
                "type": "Policy"
            }
        ],
        "Support Organizations": [
            {
                "name": "Zero Abuse Project",
                "description": "Organization dedicated to protecting children from abuse and sexual assault",
                "url": "https://zeroabuse.org/",
                "type": "Support"
            },
            {
                "name": "National Children's Alliance",
                "description": "Professional membership organization dedicated to helping local communities respond to allegations of child abuse",
                "url": "https://www.nationalchildrensalliance.org/",
                "type": "Support"
            },
            {
                "name": "Prevent Child Abuse America",
                "description": "Organization working to prevent abuse and neglect of children",
                "url": "https://preventchildabuse.org/",
                "type": "Support"
            },
            {
                "name": "Childhelp National Child Abuse Hotline",
                "description": "24/7 hotline offering crisis intervention, information, and referrals",
                "url": "https://www.childhelp.org/hotline/",
                "type": "Support",
                "phone": "1-800-4-A-CHILD (1-800-422-4453)"
            }
        ],
        "Research Centers": [
            {
                "name": "CDC Violence Prevention",
                "description": "Research and resources on child abuse and neglect prevention",
                "url": "https://www.cdc.gov/violenceprevention/childabuseandneglect/",
                "type": "Research"
            },
            {
                "name": "Child Welfare Information Gateway",
                "description": "Service of the Children's Bureau that provides access to information and resources",
                "url": "https://www.childwelfare.gov/",
                "type": "Research"
            }
        ]
    }

@st.cache_data(show_spinner=False)
def get_quiz_questions():
    """
    Load quiz questions.
    In a real app, this would load from a database or API.
    """
    return [
        {
            "question": "Neglect is the most common form of child maltreatment in the U.S.",
            "options": ["True", "False"],
            "answer": "True",
            "explanation": "Neglect accounts for approximately 76% of substantiated cases of child maltreatment."
        },
        {
            "question": "Which age group has the highest victimization rate in the U.S.?",
            "options": ["Infants under 1", "Children 1-3", "School-aged children (6-12)", "Teenagers (13-17)"],
            "answer": "Infants under 1",
            "explanation": "Infants under 1 year old have the highest rate of victimization at 24.5 per 1,000 children."
        },
        {
            "question": "Which demographic group faces the highest rates of substantiated maltreatment?",
            "options": ["White children", "African American children", "Hispanic children", "American Indian/Alaska Native children"],
            "answer": "American Indian/Alaska Native children",
            "explanation": "American Indian/Alaska Native children have the highest victim rate at about 14.3 per 1,000 children."
        },
        {
            "question": "What percentage of perpetrators of child maltreatment are parents?",
            "options": ["Around 30%", "Around 50%", "Around 75%", "Around 90%"],
            "answer": "Around 75%",
            "explanation": "Approximately 77.5% of perpetrators are parents of the victim."
        },
        {
            "question": "In the most recent data, child maltreatment fatalities have:",
            "options": ["Increased significantly", "Remained mostly stable", "Decreased significantly", "Fluctuated with no clear trend"],
            "answer": "Increased significantly",
            "explanation": "Child fatalities due to maltreatment have increased by about 17% over the past decade."
        },
        {
            "question": "Which is NOT typically considered a form of child maltreatment in official statistics?",
            "options": ["Physical abuse", "Emotional abuse", "Academic neglect", "Medical neglect"],
            "answer": "Academic neglect",
            "explanation": "While educational neglect is tracked in some states, 'academic neglect' is not a standard category in federal maltreatment statistics."
        },
        {
            "question": "What factor has the strongest correlation with increased risk of child maltreatment?",
            "options": ["Geographic location", "Socioeconomic factors", "Parental age", "Family size"],
            "answer": "Socioeconomic factors",
            "explanation": "Economic stress, poverty, and lack of social supports are strongly correlated with increased risk of child maltreatment."
        }
    ]