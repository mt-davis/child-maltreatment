import streamlit as st
import pandas as pd
import random
import time
import sys
import os

# Add the parent directory to the path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_css, display_fact_box, show_success_message
from data.data_loader import get_quiz_questions

# Page configuration
st.set_page_config(
    page_title="Child Maltreatment Data Dashboard - Quiz",
    page_icon="❓",
    layout="wide"
)

# Load custom CSS
load_css()

# Title
st.title("Test Your Knowledge: Child Maltreatment Quiz")
st.markdown("""
Test your understanding of child maltreatment data and issues with this interactive quiz.
Learn key facts while assessing your knowledge about this important topic.
""")

# Initialize or get session state for tracking quiz progress
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered_questions = []
    st.session_state.total_questions = 0
    st.session_state.quiz_completed = False

# Load quiz questions
all_questions = get_quiz_questions()

# Quiz introduction section
if not st.session_state.quiz_started and not st.session_state.quiz_completed:
    st.markdown("## Quiz Introduction")
    st.markdown("""
    This quiz will test your knowledge about child maltreatment statistics, risk factors,
    and prevention approaches. Each question explores an important aspect of understanding
    this complex issue.
    
    Ready to begin? Select the number of questions you'd like to answer and click "Start Quiz".
    """)
    
    # Quiz options
    col1, col2 = st.columns(2)
    
    with col1:
        num_questions = st.slider(
            "Number of questions:",
            min_value=3,
            max_value=len(all_questions),
            value=5,
            step=1
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        start_button = st.button("Start Quiz")
        
        if start_button:
            st.session_state.quiz_started = True
            st.session_state.total_questions = num_questions
            
            # Randomly select questions
            selected_indices = random.sample(range(len(all_questions)), num_questions)
            st.session_state.selected_questions = [all_questions[i] for i in selected_indices]
            
            # Reset other states
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered_questions = []
            
            # Force a rerun to show the first question
            st.experimental_rerun()

# Quiz in progress
elif st.session_state.quiz_started and not st.session_state.quiz_completed:
    # Get the current question
    current_q = st.session_state.current_question
    question_data = st.session_state.selected_questions[current_q]
    
    # Display progress
    progress = (current_q) / st.session_state.total_questions
    st.progress(progress)
    st.markdown(f"**Question {current_q + 1} of {st.session_state.total_questions}**")
    
    # Display the question in a styled container
    st.markdown(f"""
    <div class="quiz-question">
        <h3>{question_data['question']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show options
    selected_answer = st.radio(
        "Select your answer:",
        question_data['options'],
        key=f"question_{current_q}"
    )
    
    # Submit button
    if st.button("Submit Answer"):
        is_correct = selected_answer == question_data['answer']
        
        # Update score
        if is_correct:
            st.session_state.score += 1
            st.success(f"✓ Correct! {question_data['explanation']}")
        else:
            st.error(f"✗ Incorrect. The correct answer is: {question_data['answer']}. {question_data['explanation']}")
        
        # Store the answered question
        st.session_state.answered_questions.append({
            'question': question_data['question'],
            'user_answer': selected_answer,
            'correct_answer': question_data['answer'],
            'is_correct': is_correct,
            'explanation': question_data['explanation']
        })
        
        # Check if this was the last question
        if current_q + 1 >= st.session_state.total_questions:
            # Quiz is complete
            st.session_state.quiz_completed = True
            st.session_state.quiz_started = False
        else:
            # Move to next question
            st.session_state.current_question += 1
        
        # Force a rerun to update the page
        st.experimental_rerun()

# Quiz completed
elif st.session_state.quiz_completed:
    # Show the final score with animation
    st.markdown("## Quiz Results")
    
    # Calculate percentage
    score_percent = (st.session_state.score / st.session_state.total_questions) * 100
    
    # Display score with appropriate message
    if score_percent >= 80:
        message = "Excellent! You have a strong understanding of child maltreatment issues."
        color = "#2ecc71"  # Green
    elif score_percent >= 60:
        message = "Good job! You have a solid foundation of knowledge about child maltreatment."
        color = "#f39c12"  # Orange
    else:
        message = "Thank you for taking the quiz. There's more to learn about child maltreatment."
        color = "#3498db"  # Blue
    
    # Animated score reveal
    score_container = st.container()
    with score_container:
        st.markdown(f"""
        <div style="
            background-color: {color}15;
            border: 2px solid {color};
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        ">
            <h2 style="color: {color}; margin-top: 0;">Your Score: {st.session_state.score}/{st.session_state.total_questions} ({score_percent:.0f}%)</h2>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Review of answers
    st.markdown("## Review Your Answers")
    
    for i, item in enumerate(st.session_state.answered_questions):
        with st.expander(f"Question {i+1}: {item['question']}"):
            if item['is_correct']:
                st.markdown(f"""
                <p><span class="correct-answer">✓ You answered correctly:</span> {item['user_answer']}</p>
                <p><strong>Explanation:</strong> {item['explanation']}</p>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <p><span class="incorrect-answer">✗ Your answer:</span> {item['user_answer']}</p>
                <p><span class="correct-answer">✓ Correct answer:</span> {item['correct_answer']}</p>
                <p><strong>Explanation:</strong> {item['explanation']}</p>
                """, unsafe_allow_html=True)
    
    # Additional learning resources
    st.markdown("## Continue Learning")
    st.markdown("""
    Want to learn more about child maltreatment prevention and intervention?
    Explore these resources:
    
    - **Child Welfare Information Gateway** - [childwelfare.gov](https://www.childwelfare.gov)
    - **Centers for Disease Control and Prevention** - [cdc.gov/violenceprevention](https://www.cdc.gov/violenceprevention/childabuseandneglect/)
    - **Prevent Child Abuse America** - [preventchildabuse.org](https://preventchildabuse.org)
    """)
    
    # Option to retake the quiz
    if st.button("Take Another Quiz"):
        # Reset all quiz state
        st.session_state.quiz_started = False
        st.session_state.quiz_completed = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered_questions = []
        # Force a rerun to show the intro screen
        st.experimental_rerun()

# Key facts sidebar
st.sidebar.markdown("## Quick Facts")
st.sidebar.markdown("""
As you take the quiz, keep these key facts in mind:

- Neglect is the most common form of child maltreatment
- Younger children, particularly infants, face the highest risk
- Prevention is possible with the right supports and services
- Early intervention can significantly improve outcomes
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Child Maltreatment Data Dashboard | Data sourced from aggregated reports and research")