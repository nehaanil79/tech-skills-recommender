# A file to check for how many ads in the database has no skills.

import pandas as pd
from skills import SKILLS, build_patterns, extract_skills

CLEAN_FILE = r"C:\Users\nehaa\OneDrive\Desktop\Software_Engineer_AI_Projects\tech-skills-recommender\data\clean_jobs.csv"

df = pd.read_csv(CLEAN_FILE)
patterns = build_patterns(SKILLS)
df["skills"] = df["desc_clean"].astype(str).apply(lambda t: extract_skills(t, patterns))
empty = df[df["skills"].str.len() == 0]

print(f"Ads with no skills: {len(empty)} of {len(df)}")
print("\nAds with no skills, by title:")
print(empty["title_clean"].value_counts())

n_samples = min(5, len(empty))  
for text in empty["desc_clean"].sample(n_samples, random_state=1):
    print("\n---\n", text[:400])