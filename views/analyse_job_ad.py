import streamlit as st

st.title("Analyse a job ad")
st.write("Paste a job ad and your skills. AI pulls out what the role needs, "
         "then compares it with the job market and with you.")

with st.container(border=True):
    job_ad = st.text_area("Job ad", height=200,
                          placeholder="Paste the full job ad here: title, responsibilities and requirements")
    my_skills = st.text_input("Your skills (optional, comma-separated)",
                              placeholder="e.g. Python, SQL, Streamlit")
    analyse = st.button("Analyse job ad", type="primary")

if analyse:
    st.info("AI analysis is coming in the next step.", icon=":material/construction:")