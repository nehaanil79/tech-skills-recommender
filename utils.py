import re
from pathlib import Path

import pandas as pd
import streamlit as st

COUNTS_FILE = Path(__file__).resolve().parent / "data" / "skill_counts.csv"


@st.cache_data
def load_counts() -> pd.DataFrame:
    return pd.read_csv(COUNTS_FILE)


def is_title_skill(skill: str, title: str) -> bool:
    skill_words = re.sub(r"[^a-z0-9+#]+", " ", skill.lower()).split()
    title_words = set(re.sub(r"[^a-z0-9+#]+", " ", title.lower()).split())
    return bool(skill_words) and all(word in title_words for word in skill_words)