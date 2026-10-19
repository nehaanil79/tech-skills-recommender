import json
from groq import Groq

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """You extract information from job ads.
Return ONLY a JSON object with exactly these keys:
- "job_title": string, the role being advertised
- "seniority": one of "graduate", "junior", "mid", "senior", "unknown"
- "summary": string, 2 sentences in plain English describing the role
- "must_have": list of technical skills the ad says are required
- "nice_to_have": list of technical skills the ad says are a bonus or preferred
Rules:
- Only include skills actually written in the ad. Do not guess.
- Technical skills only (languages, tools, frameworks, methods). No soft skills like "communication".
- Use short standard names, e.g. "Python", "AWS", "Docker".
- If the ad offers alternatives (e.g. "Python, R or Java", "AWS, Azure or GCP"),
  combine them into ONE item separated by " / ", e.g. "Python / R / Java".
- Skip vague terms that are not a specific skill or tool, e.g. "GenAI tools", "AI-assisted tools", "reporting".
- If nothing fits a list, return an empty list."""

SENIORITY_LEVELS = {"graduate", "junior", "mid", "senior", "unknown"}


def clean_skill_list(value) -> list:
    if not isinstance(value, list):
        return []
    seen = set()
    cleaned = []
    for item in value:
        if not isinstance(item, str):
            continue
        skill = item.strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            cleaned.append(skill)
    return cleaned


def validate(data: dict) -> dict:
    seniority = str(data.get("seniority", "unknown")).lower()
    if seniority not in SENIORITY_LEVELS:
        seniority = "unknown"

    must_have = clean_skill_list(data.get("must_have"))
    must_lower = {s.lower() for s in must_have}
    nice_to_have = [s for s in clean_skill_list(data.get("nice_to_have"))
                    if s.lower() not in must_lower]

    return {
        "job_title": str(data.get("job_title", "")).strip() or "Unknown role",
        "seniority": seniority,
        "summary": str(data.get("summary", "")).strip(),
        "must_have": must_have,
        "nice_to_have": nice_to_have,
    }


def analyse_job_ad(job_ad: str, api_key: str) -> dict:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": job_ad},
        ],
        response_format={"type": "json_object"},
        reasoning_effort="low",
        temperature=0,
    )
    raw = response.choices[0].message.content
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("The model did not return valid JSON.") from error
    return validate(data)


if __name__ == "__main__":
    import tomllib

    with open(".streamlit/secrets.toml", "rb") as f:
        key = tomllib.load(f)["GROQ_API_KEY"]

    sample_ad = """Junior Data Scientist - Melbourne
We're looking for a graduate or junior data scientist to join our analytics team.
You'll build forecasting models and dashboards for our retail clients.
Must have: Python, SQL, pandas and experience with scikit-learn.
Nice to have: Power BI, Azure, or experience with Docker.
You're a great communicator who enjoys working in a team."""

    result = analyse_job_ad(sample_ad, key)
    print(json.dumps(result, indent=2))