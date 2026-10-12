DATA_FILE = r"C:\Users\nehaa\OneDrive\Desktop\Software_Engineer_AI_Projects\tech-skills-recommender\data\job_title_des_data.csv"
TITLE_COL = "Job Title"
DESC_COL  = "Job Description"

import pandas as pd

df = pd.read_csv(DATA_FILE)
print("Rows, Columns:",df.shape)
print("\nColumns:", list(df.columns))
print("\nMissing values:\n", df.isnull().sum())

print("\nTop 20 job titles:\n", df[TITLE_COL].value_counts().head(20))

df["desc_length"] = df[DESC_COL].str.len()
print("\nDescription length (characters):\n", df["desc_length"].describe())

print("\nSample description:\n", df[DESC_COL].iloc[0][:800])

print("Unique descriptions:", df[DESC_COL].nunique())