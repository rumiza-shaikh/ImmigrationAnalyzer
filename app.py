import streamlit as st
import plotly.express as px
import pandas as pd
from scoring import score_eligibility

st.set_page_config(page_title="ImmigrationAnalyzer", layout="centered")

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

def welcome():
    st.title("ImmigrationAnalyzer")
    st.markdown("#### Evaluate your EB1-A and EB2-NIW eligibility in minutes.")
    st.markdown("This tool gives you a visual profile, custom checklists, and letter templates to support your petition.")
    if st.button("Start Eligibility Assessment"):
        st.session_state.page = "quiz"

def quiz():
    st.header("Eligibility Assessment")
    with st.form("eligibility_form"):
        pub = st.radio("Have you published peer-reviewed articles?", ["Yes", "No"])
        media = st.radio("Have you been featured in media (news, interviews, etc.)?", ["Yes", "No"])
        judge = st.radio("Have you judged work of others?", ["Yes", "No"])
        salary = st.radio("Do you earn a salary in the top 10% of your field?", ["Yes", "No"])
        contrib = st.radio("Have you made original contributions of major significance?", ["Yes", "No"])
        awards = st.radio("Have you received prestigious national or international awards?", ["Yes", "No"])
        memberships = st.radio("Are you a member of exclusive professional associations?", ["Yes", "No"])
        display = st.radio("Has your work been exhibited or showcased publicly?", ["Yes", "No"])
        role = st.radio("Do you hold a critical role in a distinguished organization?", ["Yes", "No"])
        commercial = st.radio("Has your work led to significant commercial success or patents?", ["Yes", "No"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.responses = {
            "pub": pub, "media": media, "judge": judge, "salary": salary, "contrib": contrib,
            "awards": awards, "memberships": memberships, "display": display, "role": role, "commercial": commercial
        }
        st.session_state.page = "results"

def results():
    st.header("Your USCIS Criteria Breakdown")
    scores = score_eligibility(st.session_state.responses)
    df = pd.DataFrame({'Criterion': list(scores.keys()), 'Score': list(scores.values())})
    fig = px.bar(
        df, x='Score', y='Criterion', orientation='h',
        range_x=[0, 2], color='Score', color_continuous_scale='Blues'
    )
    fig.update_layout(yaxis_title='', xaxis_title='Score (out of 2)', height=500)
    st.plotly_chart(fig)

    st.subheader("Personalized Profile Assessment")
    feedback_map = {
        "Publications": {
            2: "Excellent — your publication record strongly supports your case.",
            1: "Good — you have some publications, but more top-tier journals could help.",
            0: "This is a gap — consider publishing in reputable journals."
        },
        "Media": {
            2: "Strong media presence — well done.",
            1: "Some coverage present — aim for higher-credibility outlets.",
            0: "Try securing interviews or media features about your work."
        },
        "Judging": {
            2: "Great — judging others’ work shows field recognition.",
            1: "Consider participating more formally in review panels.",
            0: "Apply to judge competitions or review proposals to improve this."
        },
        "Contributions": {
            2: "Well-demonstrated original impact — this is a strength.",
            1: "You have some contributions — emphasize their wider influence.",
            0: "Document unique results or innovations more clearly."
        },
        "Salary": {
            2: "High compensation is a strong supporting factor.",
            1: "Could benefit from salary benchmarking or awards.",
            0: "Try to show income or offers reflecting top-tier standing."
        },
        "Memberships": {
            2: "Prestigious memberships add solid credibility.",
            1: "Consider joining more selective, invite-only associations.",
            0: "Look into national or field-specific elite associations."
        },
        "Awards": {
            2: "Major awards strengthen your petition.",
            1: "Try applying for competitive fellowships or grants.",
            0: "Lack of awards — seek nominations or contests."
        },
        "Display of Work": {
            2: "Your work has strong visibility — keep it up.",
            1: "Increase your visibility through talks or showcases.",
            0: "Consider exhibitions, showcases, or public presentations."
        },
        "Critical Role": {
            2: "Leadership well documented — this supports your case.",
            1: "Could use clearer documentation of your influence.",
            0: "Consider showing org charts or testimonials proving your role."
        },
        "Commercial Success": {
            2: "Strong commercial results add major value.",
            1: "Emphasize more specific metrics or revenue impacts.",
            0: "Explore ways to monetize or patent your work."
        }
    }

    for crit, val in scores.items():
        st.markdown(f"**{crit}**: {feedback_map[crit][val]}")

    st.subheader("Your Personalized Evidence Checklist")
    criteria_map = {
        "pub": "Peer-reviewed publications",
        "media": "Media mentions and press coverage",
        "judge": "Judging experience at conferences or panels",
        "contrib": "Original contributions of major significance",
        "salary": "High compensation proof (offer letters, salary slips)",
        "awards": "Awards, grants, or fellowships",
        "memberships": "Memberships in selective professional associations",
        "display": "Display of work (exhibits, performances, showcases)",
        "role": "Critical role documentation (org charts, impact reports)",
        "commercial": "Patents or commercial revenue from your innovations"
    }

    missing = [v for k, v in criteria_map.items() if st.session_state.responses.get(k) == "No"]

    if missing:
        st.markdown("We recommend gathering evidence for the following:")
        for item in missing:
            st.markdown(f"- {item}")
    else:
        st.success("🎉 You’ve covered all 10 USCIS criteria. Strong case!")

    st.subheader("Letter & Statement Templates")
    template_type = st.radio("Select a template to view:", [
        "Academic Recommender Letter",
        "Industry Recommender Letter",
        "EB2-NIW Personal Statement"
    ])

    if template_type == "Academic Recommender Letter":
        st.code("""
[Professor's Name]  
[Department]  
[University Name]  
[Email Address]  
[Date]

To Whom It May Concern,

I am pleased to recommend [Candidate] for permanent residency under the [EB1-A / EB2-NIW] category. I have observed their significant contributions in [field]. Their work on [project] demonstrates excellence and global relevance.

Sincerely,  
[Professor's Name]
        """, language='markdown')

    elif template_type == "Industry Recommender Letter":
        st.code("""
[Executive's Name]  
[Title]  
[Company Name]  
[Email Address]  
[Date]

To Whom It May Concern,

I recommend [Candidate] for a green card under the [EB1-A / EB2-NIW] category. Their work on [product/project] has had measurable business impact. I fully support their petition.

Sincerely,  
[Executive's Name]
        """, language='markdown')

    elif template_type == "EB2-NIW Personal Statement":
        st.code("""
[Your Name]  
[Email Address]  
[Date]

To Whom It May Concern,

I am petitioning under the EB2-NIW category. My work in [field] advances U.S. interests such as [goal]. I’ve led projects like [X] that reflect my impact. I respectfully seek approval to continue this mission from within the U.S.

Sincerely,  
[Your Name]
        """, language='markdown')

    if st.button("Back to Home"):
        st.session_state.page = "welcome"

if st.session_state.page == "welcome":
    welcome()
elif st.session_state.page == "quiz":
    quiz()
elif st.session_state.page == "results":
    results()
