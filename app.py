import streamlit as st
import plotly.express as px
import pandas as pd
from scoring import score_eligibility

st.set_page_config(page_title="ImmigrationAnalyzer", layout="centered")

# --- Load custom CSS ---
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found.")

load_css()

if "responses" not in st.session_state:
    st.session_state.responses = {}
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# --- Welcome Page ---
def welcome():
    st.title("ImmigrationAnalyzer")
    st.markdown("#### Evaluate your EB1-A and EB2-NIW eligibility in minutes.")
    st.markdown("This tool gives you a visual profile and copy-pasteable templates to help build your self-petition case.")
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
        awards = st.radio("Have you received prestigious national or international awards?", ["Yes", "No"])
        memberships = st.radio("Are you a member of exclusive professional associations?", ["Yes", "No"])
        display = st.radio("Has your work been exhibited or showcased publicly?", ["Yes", "No"])
        role = st.radio("Do you hold a critical or leading role in a distinguished organization?", ["Yes", "No"])
        commercial = st.radio("Has your work led to significant commercial success or patents?", ["Yes", "No"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.responses = {
            "pub": pub, "media": media, "judge": judge, "salary": salary, "contrib": contrib,
            "awards": awards, "memberships": memberships, "display": display, "role": role, "commercial": commercial
        }
        st.session_state.page = "results"

# --- Results Page ---
def results():
    st.header("Your USCIS Criteria Breakdown")

    scores = score_eligibility(st.session_state.responses)

    df = pd.DataFrame({
        'Criterion': list(scores.keys()),
        'Score': list(scores.values())
    })

    fig = px.bar(
        df,
        x='Score',
        y='Criterion',
        orientation='h',
        range_x=[0, 2],
        color='Score',
        color_continuous_scale='Blues',
        title=None
    )
    fig.update_layout(
        yaxis_title='',
        xaxis_title='Score (out of 2)',
        height=500,
        margin=dict(l=40, r=30, t=30, b=30)
    )
    st.plotly_chart(fig)

    st.subheader("Suggested Evidence Checklist")
    checklist_items = [
        "✔️ Peer-reviewed publications",
        "✔️ Media mentions and press coverage",
        "✔️ Judging experience at conferences or panels",
        "✔️ Original contributions of major significance",
        "✔️ High compensation proof (offer letters, salary slips)",
        "✔️ Awards, grants, or fellowships",
        "✔️ Memberships in selective professional associations",
        "✔️ Display of work (exhibits, performances, showcases)",
        "✔️ Critical role documentation (org charts, impact reports)",
        "✔️ Patents or commercial revenue from your innovations"
    ]
    for item in checklist_items:
        st.markdown(f"- {item}")

    st.subheader("Recommendation Letter & Statement Templates")

    template_type = st.radio(
        "Select a template to view:",
        options=[
            "Academic Recommender Letter",
            "Industry Recommender Letter",
            "EB2-NIW Personal Statement"
        ]
    )

    if template_type == "Academic Recommender Letter":
        academic_template = """
[Professor's Name]  
[Department]  
[University Name]  
[Email Address]  
[Date]

To Whom It May Concern,

I am pleased to recommend [Candidate’s Full Name] for U.S. permanent residency under the [EB1-A / EB2-NIW] category. I have worked with [him/her/them] in [capacity], during which I observed [his/her/their] impactful contributions to the field of [discipline].

Their work on [describe research or innovation] has not only advanced academic thought but also holds national and global significance. [Candidate] demonstrates rare qualities of scholarly excellence, originality, and persistence that meet the high bar of this immigration category.

I strongly support this petition and am confident in [his/her/their] extraordinary potential.

Sincerely,  
[Professor’s Name]
"""
        st.code(academic_template, language='markdown')

    elif template_type == "Industry Recommender Letter":
        industry_template = """
[Executive's Name]  
[Title]  
[Company Name]  
[Email Address]  
[Date]

To Whom It May Concern,

I am writing to recommend [Candidate’s Name] for a U.S. green card under the [EB1-A / EB2-NIW] category. I have known [him/her/them] in a professional capacity as [his/her/their] [manager/partner/industry peer], and I can attest to the exceptional impact of [his/her/their] work.

[Candidate’s] contributions to [describe product, system, or strategy] have led to significant business outcomes, including [revenue impact, reach, innovation]. Their skills and leadership in [field] are exceptional and stand out even at an international level.

I wholeheartedly endorse this petition.

Sincerely,  
[Executive Name]
"""
        st.code(industry_template, language='markdown')

    elif template_type == "EB2-NIW Personal Statement":
        personal_statement = """
[Your Name]  
[Email Address]  
[Date]

To Whom It May Concern,

I am writing this personal statement in support of my petition for permanent residency under the EB2 National Interest Waiver category. My work in [field/industry] contributes directly to the United States' national goals of [e.g., technological innovation, public health, education reform].

Through projects such as [briefly describe], I have made original contributions that benefit a broad population, address systemic challenges, and foster international collaboration. My intention is to continue this work within the U.S., helping further its leadership in [specific goal].

I respectfully request favorable consideration of my petition and thank you for the opportunity to contribute to this nation.

Sincerely,  
[Your Name]
"""
        st.code(personal_statement, language='markdown')

    if st.button("Back to Home"):
        st.session_state.page = "welcome"

# --- Page Router ---
if st.session_state.page == "welcome":
    welcome()
elif st.session_state.page == "quiz":
    quiz()
elif st.session_state.page == "results":
    results()
