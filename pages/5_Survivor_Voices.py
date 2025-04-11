import streamlit as st
import pandas as pd
import random
import sys
import os
import time

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, create_quote_box, display_fact_box, generate_random_story
from data.data_loader import get_quotes

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - Survivor Voices",
    page_icon="🗣️",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("Survivor Voices")
st.markdown("""
Behind every statistic is a real person with a real story. This page centers the voices 
and experiences of survivors of child maltreatment to help humanize the data and deepen
our understanding of the impact of abuse and neglect.

*Note: All testimonials shared here are from adult survivors who have consented to share 
their stories for educational purposes.*
""")

# Load quotes data
quotes = get_quotes()

# Main content in two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Survivor Testimonials")
    st.markdown("""
    The following testimonials from adult survivors of child maltreatment provide insight into 
    their experiences, the impact of maltreatment on their lives, and what helped them in their
    healing journeys.
    """)
    
    # Display all quotes with more context and styling
    for i, quote in enumerate(quotes):
        with st.container():
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                border-left: 5px solid #3498db;
                padding: 20px;
                margin: 20px 0;
                border-radius: 0 5px 5px 0;
            ">
                <p style="font-style: italic; font-size: 1.1em;">"{quote['quote']}"</p>
                <p style="text-align: right; margin-bottom: 0;"><strong>{quote['name']}</strong>, age {quote['age']}</p>
                <p style="text-align: right; color: #7f8c8d; margin-top: 0;">{quote['background']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Interactive element for reflection
    st.markdown("## Reflection Space")
    st.markdown("""
    Take a moment to reflect on these stories and what they mean for how we approach
    child protection and support for survivors.
    """)
    
    reflection_prompt = st.selectbox(
        "Choose a reflection prompt:",
        [
            "What stood out to you in these survivor stories?",
            "How do these personal stories change your understanding of the statistics?",
            "What could have made a difference for these survivors?",
            "How might these insights inform prevention efforts?"
        ]
    )
    
    reflection = st.text_area(
        "Your reflection (private, not stored):",
        height=150,
        placeholder="Type your thoughts here..."
    )
    
    if reflection:
        st.success("Thank you for taking time to reflect on these important stories.")
    
    # Themes section
    st.markdown("## Common Themes from Survivor Experiences")
    
    # Create tabs for different themes
    theme_tab1, theme_tab2, theme_tab3, theme_tab4 = st.tabs([
        "Missed Opportunities", 
        "Importance of One Person", 
        "Long-term Impact",
        "Resilience & Healing"
    ])
    
    with theme_tab1:
        st.markdown("""
        ### Missed Opportunities for Intervention
        
        Many survivors share stories of "missed signals" - moments when someone could have noticed
        and intervened, but didn't. These include:
        
        - Teachers noticing behavioral changes or physical signs
        - Healthcare providers seeing injuries or concerning symptoms
        - Neighbors aware of concerning situations but unsure how to respond
        - Family members who suspected something was wrong
        
        These stories highlight the importance of training for mandatory reporters and raising
        awareness about how to respond to concerns about a child's welfare.
        """)
        
        display_fact_box(
            "Key Insight", 
            "Many survivors report that they showed signs that were missed or misinterpreted by adults around them."
        )
    
    with theme_tab2:
        st.markdown("""
        ### The Importance of One Caring Adult
        
        A consistent theme in survivor stories is the profound impact that even one supportive
        adult can have. This might be:
        
        - A teacher who provided a safe space at school
        - A coach who offered consistency and positive attention
        - A relative who eventually intervened
        - A counselor who validated their experiences
        
        This reinforces research showing that having even one stable, caring adult relationship
        can significantly buffer against the effects of adverse childhood experiences.
        """)
        
        display_fact_box(
            "Key Insight", 
            "The presence of even one reliable, supportive adult can be a powerful protective factor for children experiencing maltreatment."
        )
    
    with theme_tab3:
        st.markdown("""
        ### Long-term Impact Across Life Domains
        
        Survivors often describe effects that extend far beyond childhood, including:
        
        - Challenges with trust and relationships
        - Mental health impacts including depression, anxiety, and PTSD
        - Physical health consequences
        - Educational and economic impacts
        
        These accounts align with the Adverse Childhood Experiences (ACEs) research showing
        the potential long-term health and wellbeing impacts of childhood trauma.
        """)
        
        display_fact_box(
            "Key Insight", 
            "The effects of child maltreatment can persist long into adulthood, affecting mental health, physical health, relationships, and economic stability."
        )
    
    with theme_tab4:
        st.markdown("""
        ### Resilience and Pathways to Healing
        
        Despite the challenges, many survivors share stories of resilience and healing:
        
        - Finding purpose in advocacy and helping others
        - The transformative impact of therapy and support groups
        - Building healthy relationships that provide healing experiences
        - Reconnecting with cultural or spiritual traditions
        
        These stories offer hope and underscore the importance of trauma-informed services
        that support resilience and recovery.
        """)
        
        display_fact_box(
            "Key Insight", 
            "With appropriate support, survivors demonstrate remarkable resilience and capacity for healing and growth."
        )

with col2:
    # Statistics in context
    st.markdown("## Statistics in Human Context")
    st.markdown("""
    The personal stories on this page help us understand what the statistics really mean
    in human terms. Each number represents a child with a unique experience and story.
    """)
    
    # Create an animation that "humanizes" a statistic
    st.markdown("### Behind the Numbers")
    
    if st.button("Explore a Story Behind the Numbers"):
        with st.spinner("Creating a story..."):
            time.sleep(1)  # Brief delay for animation effect
            
            # Display a randomly generated story
            story = generate_random_story()
            
            # Display the story in a styled container
            st.markdown(f"""
            <div style="
                background-color: #f0f9ff;
                border: 1px solid #3498db;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            ">
                <h4 style="color: #3498db; margin-top: 0;">A Story Behind the Statistics</h4>
                <p>{story}</p>
                <p style="font-style: italic; color: #7f8c8d; margin-bottom: 0;">
                    This is a representative narrative based on common patterns in child maltreatment cases.
                    It is not a real case but reflects experiences shared by many children.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Resources for survivors
    st.markdown("## Resources for Survivors")
    
    st.markdown("""
    If you are a survivor of child maltreatment, know that you are not alone.
    Resources are available to support healing and recovery:
    
    - **National Child Traumatic Stress Network**  
      [www.nctsn.org](https://www.nctsn.org)  
      Information and resources about childhood trauma
      
    - **RAINN (Rape, Abuse & Incest National Network)**  
      [www.rainn.org](https://www.rainn.org) | 1-800-656-HOPE (4673)  
      Support for survivors of sexual violence
      
    - **Adult Survivors of Child Abuse**  
      [www.ascasupport.org](https://www.ascasupport.org)  
      Recovery resources and support groups
      
    - **Childhelp National Child Abuse Hotline**  
      1-800-4-A-CHILD (1-800-422-4453)  
      Crisis intervention and professional counseling
    """)
    
    # Call to action
    st.markdown("""
    <div style="
        background-color: #e8f8f5;
        border-left: 5px solid #2ecc71;
        padding: 15px;
        margin: 20px 0;
        border-radius: 0 5px 5px 0;
    ">
        <h4 style="color: #27ae60; margin-top: 0;">Share Your Story</h4>
        <p>
            Survivor voices are powerful catalysts for change. If you are a survivor and wish to share your story to help educate others, consider reaching out to child advocacy organizations that provide platforms for survivor perspectives.
        </p>
    </div>
    """, unsafe_allow_html=True)

# A note on ethical storytelling
st.markdown("## A Note on Ethical Storytelling")
st.markdown("""
This page aims to center survivor voices while respecting privacy and dignity.
All stories shared are from adult survivors who have consented to share their
experiences for educational purposes.

It's important to approach these stories with respect and to recognize that each
survivor's experience is unique. While these stories help illustrate the impact
of maltreatment, they should not be used to make generalizations or assumptions.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")