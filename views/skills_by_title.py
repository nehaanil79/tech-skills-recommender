import plotly.express as px
import streamlit as st

from skills.skills import SKILLS
from utils import is_title_skill, load_counts

st.title("Which skills do employers want?")
st.write("Choose a job title to see the skills mentioned most often in real job ads.")

counts = load_counts()

# Summary cards
per_title = counts.drop_duplicates("title")
col1, col2, col3 = st.columns(3)
col1.metric("Ads analysed", f"{per_title['total_ads'].sum():,}")
col2.metric("Job titles", per_title["title"].nunique())
col3.metric("Skills tracked", len(SKILLS))

# Controls
with st.container(border=True):
    c1, c2, c3 = st.columns([2, 2, 1.5])
    title = c1.selectbox("Job title", sorted(counts["title"].unique()))
    top_n = c2.slider("Number of skills to show", min_value=5, max_value=20, value=10)
    hide_obvious = c3.checkbox("Hide skills that repeat the job title", value=True)

data = counts[counts["title"] == title]
if hide_obvious:
    data = data[~data["skill"].apply(lambda s: is_title_skill(s, title))]
data = data.sort_values("pct", ascending=False).head(top_n)

total_ads = int(per_title.loc[per_title["title"] == title, "total_ads"].iloc[0])

# Chart
with st.container(border=True):
    st.subheader(f"Top skills for {title}")
    st.caption(f"Based on {total_ads} job ads")

    fig = px.bar(
        data.sort_values("pct"),
        x="pct",
        y="skill",
        orientation="h",
        text="pct",
        color="pct",
        color_continuous_scale=["#9DB4F0", "#1D4ED8"],
        labels={"pct": "% of ads mentioning the skill", "skill": ""},
    )
    fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    fig.update_layout(
        height=40 * len(data) + 120,
        xaxis_range=[0, 100],
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

st.download_button(
    label="Download results as CSV",
    data=data[["skill", "n_ads", "pct"]].to_csv(index=False),
    file_name=f"{title.replace(' ', '_')}_skills.csv",
    mime="text/csv",
    icon=":material/download:",
)