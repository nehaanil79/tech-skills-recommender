import streamlit as st

st.set_page_config(page_title="Tech Skills Recommender", page_icon=":material/insights:", layout="wide")

pages = [
    st.Page("views/skills_by_title.py", title="Skills by job title", icon=":material/bar_chart:"),
    st.Page("views/analyse_job_ad.py", title="Analyse a job ad", icon=":material/smart_toy:"),
]

nav = st.navigation(pages)
nav.run()