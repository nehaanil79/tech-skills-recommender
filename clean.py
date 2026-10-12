import re
import pandas as pd


DATA_FILE = r"C:\Users\nehaa\OneDrive\Desktop\Software_Engineer_AI_Projects\tech-skills-recommender\data\job_title_des_data.csv"
TITLE_COL = "Job Title"
DESC_COL = "Job Description"
OUT_FILE = r"C:\Users\nehaa\OneDrive\Desktop\Software_Engineer_AI_Projects\tech-skills-recommender\data\clean_jobs.csv"


BOILERPLATE_PATTERNS = [
    r"^job types?:", r"^salary:", r"^pay:", r"^benefits:", r"^schedule:",
    r"^supplemental pay", r"^work remotely", r"^covid", r"^housing rent",
    r"^industry:", r"^ability to (commute|relocate)", r"^application deadline",
    r"^expected start date", r"^speak with the employer", r"^contract length",
    r"^work location",
]


BENEFIT_LINES = {
    "flexible schedule", "food allowance", "day shift", "night shift",
    "morning shift", "fixed shift", "monday to friday", "joining bonus",
    "overtime pay", "performance bonus", "yearly bonus", "health insurance",
    "paid sick time", "paid time off", "provident fund", "work from home",
    "cell phone reimbursement", "internet reimbursement", "leave encashment",
    "life insurance", "yes", "no",
}


def clean_title(title: str) -> str:
    title = str(title).lower().strip()
    return re.sub(r"\s+", " ", title)


def clean_description(text: str) -> str:
    text = str(text)
    text = re.sub(r"<[^>]+>", " ", text)            
    text = re.sub(r"http\S+|www\.\S+", " ", text)    

    kept_lines = []
    skipping = False
    for line in text.splitlines():
        line = line.strip().lower()
        if not line:
            continue
        is_header = line.endswith(":")
        if any(re.match(p, line) for p in BOILERPLATE_PATTERNS):
            skipping = True      
            continue
        if is_header:
            skipping = False     
        if skipping or line in BENEFIT_LINES:
            continue
        kept_lines.append(line)

    text = " ".join(kept_lines)
    text = re.sub(r"[^a-z0-9+#./\- ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main():
    df = pd.read_csv(DATA_FILE)
    rows_before = len(df)

    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df = df.drop_duplicates(subset=[TITLE_COL, DESC_COL])
    rows_after_dedup = len(df)

    df["title_clean"] = df[TITLE_COL].apply(clean_title)
    df["desc_clean"] = df[DESC_COL].apply(clean_description)

    
    df = df[df["desc_clean"].str.len() > 50]

    print(f"Rows: {rows_before} -> {rows_after_dedup} after dedup -> {len(df)} final")
    print(f"Avg description length: {df[DESC_COL].str.len().mean():.0f} -> "
          f"{df['desc_clean'].str.len().mean():.0f} characters")
    print("\nTitles:", sorted(df["title_clean"].unique()))

    
    for skill in ["c++", "c#", "node.js", "ci/cd"]:
        n = df["desc_clean"].str.contains(skill, regex=False).sum()
        print(f"Ads mentioning {skill}: {n}")

    print("\n--- BEFORE ---\n", df[DESC_COL].iloc[0][:500])
    print("\n--- AFTER ---\n", df["desc_clean"].iloc[0][:500])

    df[["title_clean", "desc_clean"]].to_csv(OUT_FILE, index=False)
    print(f"\nSaved cleaned data to {OUT_FILE}")


if __name__ == "__main__":
    main()