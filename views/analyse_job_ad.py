import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from llm import analyse_job_ad


def show_skills(label: str, skills: list, colour: str):
    st.subheader(label)
    if skills:
        st.markdown(" ".join(f":{colour}-background[{s}]" for s in skills))
    else:
        st.caption("None mentioned.")


st.title("Analyse a job ad")
st.write("Paste a job ad and AI will pull out the role, seniority and the skills it asks for.")

with st.container(border=True):
    job_ad = st.text_area("Job ad", height=250, placeholder="Paste the full job ad here...")
    my_skills = st.text_input("Your skills (optional, comma-separated)", placeholder="e.g. Python, SQL, Azure")
    analyse = st.button("Analyse job ad", type="primary", icon=":material/auto_awesome:")

if analyse:
    if len(job_ad.strip()) < 100:
        st.warning("Please paste the full job ad (at least a few sentences).")
    else:
        with st.spinner("Reading the job ad..."):
            try:
                st.session_state["result"] = analyse_job_ad(job_ad, st.secrets["GROQ_API_KEY"])
            except Exception as error:
                st.session_state.pop("result", None)
                st.error(f"Something went wrong: {error}")

result = st.session_state.get("result")

if result:
    col1, col2 = st.columns(2)
    col1.metric("Role", result["job_title"])
    col2.metric("Seniority", result["seniority"].title())

    with st.container(border=True):
        st.subheader("Summary")
        st.write(result["summary"] or "No summary returned.")

    with st.container(border=True):
        show_skills("Must have", result["must_have"], "blue")
        show_skills("Nice to have", result["nice_to_have"], "gray")