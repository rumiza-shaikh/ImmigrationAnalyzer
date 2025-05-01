import streamlit as st
import pandas as pd
from scoring import score_eligibility
import plotly.graph_objects as go

# --- Set Page Config ---
st.set_page_config(
    page_title="ImmigrationAnalyzer",
    layout="centered"
)

# --- Load Custom CSS ---
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. Using default styling.")

load_css()

# --- Session State Setup ---
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# --- Welcome Page ---
def welcome():
    st.title("ImmigrationAnalyzer")
    st.markdown("#### Analyze your EB1-A or EB2-NIW eligibility in minutes.")
    st.markdown("This tool helps you evaluate your self-petition readiness and provides a personalized roadmap.")
    
    if st.button("Start Eligibility Assessment"):
        st.session_state.page = "quiz"

# --- Quiz Page ---
def quiz():
    st.header("Eligibility Assessment")

    with st.form("eligibility_form"):
        pub = st.radio("Have you published peer-reviewed articles?", ["Yes", "No"])
        media = st.radio("Have you been featured in media (news, interviews, etc.)?", ["Yes", "No"])
        judge = st.radio("Have you judged work of others (conferences, panels)?", ["Yes", "No"])
        salary = st.radio("Do you earn a salary in the top 10% of your field?", ["Yes", "No"])
        contrib = st.radio("Have you made original contributions of major significance?", ["Yes", "No"])

        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.responses = {
            "pub": pub,
            "media": media,
            "judge": judge,
            "salary": salary,
            "contrib": contrib
        }
        st.session_state.page = "results"

# --- Results Page ---
def results():
    st.header("Your Eligibility Profile")

    scores = score_eligibility(st.session_state.responses)

    categories = list(scores.keys())
    values = list(scores.values())

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(color='rgb(0,123,255)')
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig)

    st.markdown(f"**EB1-A Fit Score:** {scores['EB1-A']} / 10")
    st.markdown(f"**EB2-NIW Fit Score:** {scores['EB2-NIW']} / 10")

    if st.button("Back to Home"):
        st.session_state.page = "welcome"

# --- Router ---
if st.session_state.page == "welcome":
    welcome()
elif st.session_state.page == "quiz":
    quiz()
elif st.session_state.page == "results":
    results()
