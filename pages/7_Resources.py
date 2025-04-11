import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, create_resource_card
from data.data_loader import get_resources

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - Resources",
    page_icon="📚",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("Resource Hub")
st.markdown("""
This resource hub provides access to prevention programs, policies, support resources, 
and research related to child maltreatment. Use the filters to find the resources most
relevant to your needs or interests.
""")

# Load resources data
resources = get_resources()

# Create filters sidebar
st.sidebar.markdown("## Filter Resources")

# Resource type filter
resource_types = ["All Types", "Prevention", "Policy", "Support", "Research"]
selected_type = st.sidebar.selectbox("Resource Type:", resource_types)

# Search functionality
search_query = st.sidebar.text_input("Search Resources:", placeholder="Enter keywords...")

# Main content
st.markdown("## Available Resources")

# Create tabs for different resource categories
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Prevention Programs", 
    "📜 Policies & Legislation", 
    "🤝 Support Organizations", 
    "🔍 Research Centers"
])

# Helper function to filter resources
def filter_resources(resources, category, resource_type, search_query):
    filtered = resources[category]
    
    # Apply resource type filter if not "All Types"
    if resource_type != "All Types":
        filtered = [r for r in filtered if r["type"] == resource_type]
    
    # Apply search filter if provided
    if search_query:
        filtered = [r for r in filtered if search_query.lower() in r["name"].lower() 
                   or search_query.lower() in r["description"].lower()]
    
    return filtered

# Display resources in each tab
with tab1:
    st.markdown("### Prevention Programs")
    st.markdown("""
    These evidence-based programs aim to prevent child maltreatment through parent education,
    family support, home visiting, and other strategies.
    """)
    
    # Filter prevention programs
    prevention_programs = filter_resources(resources, "Prevention Programs", selected_type, search_query)
    
    if prevention_programs:
        for program in prevention_programs:
            create_resource_card(
                program["name"],
                program["description"],
                program["url"],
                program["type"]
            )
    else:
        st.info("No prevention programs match your current filters.")

with tab2:
    st.markdown("### Policies & Legislation")
    st.markdown("""
    Key policies and legislation that shape child protection systems and guide prevention
    and intervention efforts at federal, state, and local levels.
    """)
    
    # Filter policies
    policies = filter_resources(resources, "Policies & Legislation", selected_type, search_query)
    
    if policies:
        for policy in policies:
            create_resource_card(
                policy["name"],
                policy["description"],
                policy["url"],
                policy["type"]
            )
    else:
        st.info("No policies match your current filters.")

with tab3:
    st.markdown("### Support Organizations")
    st.markdown("""
    Organizations providing direct services, advocacy, and resources for children,
    families, and survivors of child maltreatment.
    """)
    
    # Filter support organizations
    support_orgs = filter_resources(resources, "Support Organizations", selected_type, search_query)
    
    if support_orgs:
        for org in support_orgs:
            # Check if the organization has a phone number
            phone = org.get("phone", None)
            create_resource_card(
                org["name"],
                org["description"],
                org["url"],
                org["type"],
                phone
            )
    else:
        st.info("No support organizations match your current filters.")

with tab4:
    st.markdown("### Research Centers")
    st.markdown("""
    Research institutions and centers that provide data, analysis, and evidence-based
    recommendations on child maltreatment prevention and intervention.
    """)
    
    # Filter research centers
    research_centers = filter_resources(resources, "Research Centers", selected_type, search_query)
    
    if research_centers:
        for center in research_centers:
            create_resource_card(
                center["name"],
                center["description"],
                center["url"],
                center["type"]
            )
    else:
        st.info("No research centers match your current filters.")

# Emergency resources highlight
st.markdown("## Emergency Resources")
st.markdown("""
<div style="
    background-color: #fdedec;
    border: 2px solid #e74c3c;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
">
    <h3 style="color: #e74c3c; margin-top: 0;">If You Suspect Child Abuse or Neglect</h3>
    <p><strong>Childhelp National Child Abuse Hotline:</strong> 1-800-4-A-CHILD (1-800-422-4453)</p>
    <p>Available 24/7 with professional crisis counselors who can provide assistance in over 170 languages.</p>
    <p><strong>In an emergency situation:</strong> Call 911</p>
    <p><strong>To report suspected abuse:</strong> Contact your local child protective services agency or law enforcement.</p>
</div>
""", unsafe_allow_html=True)

# Interactive resource categorization
st.markdown("## Understanding Resource Types")

# Create columns for different resource types
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="
        background-color: #e8f8f5;
        border-top: 4px solid #2ecc71;
        padding: 15px;
        height: 200px;
        border-radius: 5px;
    ">
        <h4>Prevention Resources</h4>
        <p>Focused on stopping maltreatment before it occurs through:</p>
        <ul>
            <li>Parent education</li>
            <li>Home visiting programs</li>
            <li>Family support services</li>
            <li>Public awareness campaigns</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background-color: #eaf2f8;
        border-top: 4px solid #3498db;
        padding: 15px;
        height: 200px;
        border-radius: 5px;
    ">
        <h4>Policy Resources</h4>
        <p>Creating systemic change through:</p>
        <ul>
            <li>Legislation</li>
            <li>Funding mechanisms</li>
            <li>Government programs</li>
            <li>Standards and regulations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background-color: #fcf3cf;
        border-top: 4px solid #f39c12;
        padding: 15px;
        height: 200px;
        border-radius: 5px;
    ">
        <h4>Support Resources</h4>
        <p>Providing direct assistance through:</p>
        <ul>
            <li>Crisis hotlines</li>
            <li>Trauma treatment</li>
            <li>Family preservation services</li>
            <li>Survivor support groups</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
        background-color: #f4ecf7;
        border-top: 4px solid #8e44ad;
        padding: 15px;
        height: 200px;
        border-radius: 5px;
    ">
        <h4>Research Resources</h4>
        <p>Advancing knowledge through:</p>
        <ul>
            <li>Data collection and analysis</li>
            <li>Program evaluation</li>
            <li>Evidence-based practice</li>
            <li>Policy research</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Suggest a resource
st.markdown("## Suggest a Resource")
st.markdown("""
Do you know of a helpful resource that's not listed here? Please tell us about it!
While this dashboard is for demonstration purposes only, in a real implementation,
this form would allow users to submit resource suggestions.
""")

col1, col2 = st.columns(2)

with col1:
    resource_name = st.text_input("Resource Name:")
    resource_type = st.selectbox("Resource Type:", ["Prevention", "Policy", "Support", "Research"])
    resource_url = st.text_input("Website URL:")

with col2:
    resource_description = st.text_area("Brief Description:", height=124)
    
submit_button = st.button("Submit Resource Suggestion")

if submit_button:
    if resource_name and resource_description and resource_url:
        st.success("Thank you for your suggestion! In a real implementation, this would be reviewed and potentially added to our resource database.")
    else:
        st.warning("Please fill in all required fields.")

# Data sources and information
with st.expander("About These Resources"):
    st.markdown("""
    ### Resource Inclusion Criteria
    
    The resources included in this hub meet the following criteria:
    
    - **Evidence-Based:** Programs and approaches backed by research evidence
    - **Accessibility:** Resources that are accessible to the public
    - **Relevance:** Direct connection to child maltreatment prevention, intervention, or recovery
    - **Credibility:** Organizations with established expertise and reputation in the field
    
    ### Disclaimer
    
    The inclusion of resources in this hub does not constitute an endorsement. This dashboard
    is for educational purposes, and users should evaluate resources based on their specific needs.
    
    In a real implementation, resources would be regularly reviewed and updated to ensure
    accuracy and relevance.
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")