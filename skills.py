import re
import pandas as pd

CLEAN_FILE = r"C:\Users\nehaa\OneDrive\Desktop\Software_Engineer_AI_Projects\tech-skills-recommender\data\clean_jobs.csv"
OUT_FILE = r"C:\Users\nehaa\OneDrive\Desktop\Software_Engineer_AI_Projects\tech-skills-recommender\data\skill_counts.csv"


SKILLS = {
    # Languages
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "es6"],
    "TypeScript": ["typescript"],
    "PHP": ["php"],
    "C++": ["c++"],
    "C#": ["c#"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "Dart": ["dart"],
    "Go": ["golang"],
    "SQL": ["sql"],
    # Frontend
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular", "angularjs"],
    "Vue.js": ["vue", "vue.js", "vuejs"],
    "jQuery": ["jquery"],
    # Backend & frameworks
    "Node.js": ["node.js", "nodejs", "node js"],
    "Express.js": ["express.js", "expressjs", "express"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Spring Boot": ["spring boot", "spring"],
    "Laravel": ["laravel"],
    ".NET": ["asp.net", ".net", "dotnet"],
    "Flutter": ["flutter"],
    "WordPress": ["wordpress"],
    "REST APIs": ["rest api", "rest apis", "restful"],
    "GraphQL": ["graphql"],
    # Databases
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "Oracle": ["oracle"],
    "SQL Server": ["sql server", "mssql"],
    "Redis": ["redis"],
    # Cloud & DevOps
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Jenkins": ["jenkins"],
    "CI/CD": ["ci/cd", "ci cd", "continuous integration"],
    "Terraform": ["terraform"],
    "Ansible": ["ansible"],
    "Linux": ["linux", "unix"],
    "Git": ["git", "github", "gitlab", "bitbucket"],
    # Data & ML
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "opencv"],
    # Networking & mobile
    "TCP/IP": ["tcp/ip", "tcp ip"],
    "Firewalls": ["firewall", "firewalls"],
    "Cisco": ["cisco", "ccna"],
    "iOS": ["ios"],
    "Android": ["android"],
    "Xcode": ["xcode"],
    # Ways of working
    "Agile": ["agile", "scrum"],
}


def build_patterns(skills: dict) -> dict:
    """Compile one regex per skill that matches any alias as a whole word."""
    patterns = {}
    for skill, aliases in skills.items():
        ordered = sorted(aliases, key=len, reverse=True)
        alternatives = "|".join(re.escape(a) for a in ordered)
        patterns[skill] = re.compile(rf"(?<![a-z0-9])(?:{alternatives})(?![a-z0-9+#])")
    return patterns


def extract_skills(text: str, patterns: dict) -> set:
    """Return the set of skills mentioned at least once in the text."""
    return {skill for skill, pattern in patterns.items() if pattern.search(text)}


def main():
    df = pd.read_csv(CLEAN_FILE)
    patterns = build_patterns(SKILLS)

    df["skills"] = df["desc_clean"].astype(str).apply(lambda t: extract_skills(t, patterns))
    no_skills = (df["skills"].str.len() == 0).sum()
    print(f"Ads where no skills were found: {no_skills} of {len(df)}")

    rows = []
    for title, group in df.groupby("title_clean"):
        total_ads = len(group)
        counts = group["skills"].explode().value_counts()
        for skill, n_ads in counts.items():
            rows.append({
                "title": title,
                "skill": skill,
                "n_ads": n_ads,
                "pct": round(100 * n_ads / total_ads, 1),
                "total_ads": total_ads,
            })

    result = pd.DataFrame(rows).sort_values(["title", "pct"], ascending=[True, False])
    result.to_csv(OUT_FILE, index=False)
    print(f"Saved {len(result)} rows to {OUT_FILE}")

    for title in ["machine learning", "devops engineer", "flutter developer"]:
        print(f"\n=== {title} ===")
        top = result[result["title"] == title].head(10)
        print(top[["skill", "n_ads", "pct"]].to_string(index=False))


if __name__ == "__main__":
    main()