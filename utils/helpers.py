import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime

def load_css():
    """
    Load custom CSS styles.
    In a real app, this would load from a CSS file.
    """
    st.markdown("""
    <style>
        /* Custom styling for the dashboard */
        
        /* Page header */
        .stApp header {
            background-color: #f0f2f6;
        }
        
        /* Main title styling */
        h1 {
            color: #2c3e50;
            padding-bottom: 20px;
            border-bottom: 2px solid #e74c3c;
            margin-bottom: 30px;
        }
        
        /* Section headers */
        h2 {
            color: #3498db;
            margin-top: 35px;
            margin-bottom: 15px;
        }
        
        /* Sub-section headers */
        h3 {
            color: #2c3e50;
            margin-top: 25px;
        }
        
        /* Quote styling */
        blockquote {
            background-color: #f9f9f9;
            border-left: 5px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        
        /* Custom container for story elements */
        .story-container {
            background-color: #f5f7f9;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #e74c3c;
            margin: 20px 0;
        }
        
        /* Highlight important statistics */
        .stat-highlight {
            font-weight: bold;
            color: #e74c3c;
        }
        
        /* Survivor quote styling */
        .survivor-quote {
            font-style: italic;
            background-color: #eaf2f8;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        /* Resource card styling */
        .resource-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            transition: transform 0.3s ease;
        }
        
        .resource-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        /* Footer styling */
        footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
            font-size: 0.8em;
        }
        
        /* Tooltip styling */
        .tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted #3498db;
            cursor: help;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #34495e;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        /* Quiz styling */
        .quiz-question {
            background-color: #f5f7f9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .correct-answer {
            color: #27ae60;
            font-weight: bold;
        }
        
        .incorrect-answer {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

def format_large_number(num):
    """Format large numbers with commas."""
    return "{:,}".format(num)

def create_story_container(content, title=None):
    """Create a styled container for narrative elements."""
    html = f"""
    <div class="story-container">
        {f"<h4>{title}</h4>" if title else ""}
        {content}
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

def create_quote_box(quote, author=None, role=None):
    """Create a styled quote box."""
    html = f"""
    <blockquote class="survivor-quote">
        "{quote}"
        {f"<br><strong>— {author}</strong>" if author else ""}
        {f"<br><em>{role}</em>" if role else ""}
    </blockquote>
    """
    return st.markdown(html, unsafe_allow_html=True)

def create_resource_card(name, description, url, resource_type=None, phone=None):
    """Create a styled resource card with link."""
    html = f"""
    <div class="resource-card">
        <h4><a href="{url}" target="_blank">{name}</a></h4>
        {f"<span style='background-color: #eaf2f8; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;'>{resource_type}</span>" if resource_type else ""}
        <p>{description}</p>
        {f"<p><strong>Phone:</strong> {phone}</p>" if phone else ""}
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

def highlight_stat(value, text=None):
    """Add highlighting to important statistics."""
    if text:
        return f'<span class="stat-highlight">{value}</span> {text}'
    else:
        return f'<span class="stat-highlight">{value}</span>'

def create_tooltip(text, tooltip_text):
    """Create an inline tooltip for definitions or explanations."""
    html = f"""
    <div class="tooltip">{text}
        <span class="tooltiptext">{tooltip_text}</span>
    </div>
    """
    return html

def generate_random_story(state=None, year=None):
    """
    Generate a semi-random narrative about a child maltreatment case for storytelling.
    For narrative/educational purposes only - not real cases.
    """
    # Child profiles
    profiles = [
        {"name": "Alex", "age": "8", "gender": "male"},
        {"name": "Emma", "age": "5", "gender": "female"},
        {"name": "Jayden", "age": "3", "gender": "male"},
        {"name": "Sophia", "age": "10", "gender": "female"},
        {"name": "Miguel", "age": "7", "gender": "male"},
        {"name": "Ava", "age": "2", "gender": "female"},
        {"name": "Ethan", "age": "11", "gender": "male"},
        {"name": "Zoe", "age": "6", "gender": "female"}
    ]
    
    # Types of maltreatment
    maltreatment_types = ["neglect", "physical abuse", "emotional abuse"]
    
    # Reporter types
    reporters = ["teacher", "neighbor", "doctor", "relative", "coach"]
    
    # Intervention options
    interventions = [
        "family support services", 
        "parenting classes", 
        "substance abuse treatment", 
        "mental health counseling",
        "temporary removal and foster care placement"
    ]
    
    # Outcomes
    outcomes = [
        "remained with family with supports in place",
        "was temporarily placed with relatives",
        "entered foster care but later reunified with family",
        "was adopted by a loving family"
    ]
    
    # Select random elements
    profile = random.choice(profiles)
    maltreatment = random.choice(maltreatment_types)
    reporter = random.choice(reporters)
    intervention = random.choice(interventions)
    outcome = random.choice(outcomes)
    
    # Use provided state and year if available
    state_text = f"in {state}" if state else "in one state"
    year_text = f"In {year}" if year else "In recent years"
    
    # Construct the narrative
    story = f"""
    {year_text}, {profile['name']}, a {profile['age']}-year-old {profile['gender']} {state_text}, 
    was identified as experiencing {maltreatment}. A concerned {reporter} noticed warning signs 
    and reported the situation to child protective services. After investigation, 
    {intervention} was provided to the family. Eventually, {profile['name']} {outcome}.
    
    This represents just one example of how data translates to real children's lives.
    Each case is unique, but behind every statistic is a child like {profile['name']}.
    """
    
    return story

def display_fact_box(title, content):
    """Display a styled fact box."""
    st.markdown(f"""
    <div style="
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        background-color: #eaf2f8;
    ">
        <h4 style="color: #2c3e50; margin-top: 0;">{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)
    
def show_success_message(message):
    """Show a consistent success message with animation."""
    success_placeholder = st.empty()
    with success_placeholder.container():
        for i in range(10):
            progress = i / 10
            if progress < 1.0:
                st.progress(progress)
            time.sleep(0.05)
        st.success(message)

def create_tabs_with_icon(tab_labels, icons):
    """Create tabs with icons."""
    tabs_html = "<div class='stTabs'><div data-testid='stHorizontalTabs' role='tablist' class='st-eb st-ec st-ed st-bk st-ee st-ef'>"
    for i, (label, icon) in enumerate(zip(tab_labels, icons)):
        tabs_html += f"<button kind='tab' aria-selected='false' role='tab' tabindex='-1' class='st-ek st-bs st-el st-em st-en st-eo st-ep st-eq st-er st-ch st-cj st-es st-ck st-et st-eu st-ev st-ew st-du st-ex st-ey st-ez st-f0 st-f1'><p>{icon} {label}</p></button>"
    tabs_html += "</div></div>"
    return st.markdown(tabs_html, unsafe_allow_html=True)

def combine_charts(chart1, chart2, title=""):
    """Combine two altair charts side by side with a common title."""
    combined = alt.hconcat(chart1, chart2, title=title)
    return combined

def create_comparison_bar(value, max_value, label, color="#3498db"):
    """Create a horizontal comparison bar."""
    percent = (value / max_value) * 100
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 150px; font-weight: bold;">{label}</div>
            <div style="flex-grow: 1; margin: 0 10px;">
                <div style="background-color: #eee; border-radius: 5px; height: 20px;">
                    <div style="width: {percent}%; background-color: {color}; height: 20px; border-radius: 5px;"></div>
                </div>
            </div>
            <div style="width: 50px; text-align: right;">{value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def animate_stat_reveal(key, base_value, final_value, prefix="", suffix="", duration=2.0):
    """Animate a statistic gradually increasing from base to final value."""
    import time
    
    placeholder = st.empty()
    steps = 20
    delay = duration / steps
    
    for i in range(steps + 1):
        current = base_value + (final_value - base_value) * (i / steps)
        placeholder.markdown(f"<h3>{prefix}{int(current):,}{suffix}</h3>", unsafe_allow_html=True)
        time.sleep(delay)
    
    return placeholder

def create_impact_visualization(number, icon="👧", title="Children Affected", description=""):
    """Create a visual representation of impact using icons."""
    # Limit the number of icons to display
    display_count = min(number, 100)
    
    # Calculate how many icons to show
    icons_html = icon * display_count
    
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0; background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
        <h3>{title}</h3>
        <div style="font-size: 1.2rem; letter-spacing: 5px; line-height: 1.5; margin: 15px 0;">
            {icons_html}
        </div>
        <p><strong>{number:,}</strong> {description}</p>
    </div>
    """, unsafe_allow_html=True)