import re
import pandas as pd
import streamlit as st

COUNTS_FILE = r"data\skill_counts.csv"


@st.cache_data
def load_counts() -> pd.DataFrame:
    """Load the per-title skill percentages produced by skills.py."""
    return pd.read_csv(COUNTS_FILE)


def is_title_skill(skill: str, title: str) -> bool:
    """True if the skill just repeats the job title, e.g. 'Flutter' for 'flutter developer'."""
    skill_words = re.sub(r"[^a-z0-9+#]+", " ", skill.lower()).split()
    title_words = re.sub(r"[^a-z0-9+#]+", " ", title.lower()).split()
    return all(word in title_words for word in skill_words)