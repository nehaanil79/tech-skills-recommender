# Tech Skills Recommender

**Live app:** https://tech-skills-recommender-neha.streamlit.app/

A Streamlit app that shows which technical skills employers ask for, and uses an LLM to analyse any job ad you paste in.

## What it does

**1. Skills by job title**
Pick one of 15 tech job titles and see the skills mentioned most often across 2,159 real job ads, shown as the percentage of ads that mention each skill. You can choose how many skills to show, hide skills that just repeat the job title, and download the results as CSV.

**2. Analyse a job ad (AI)**
Paste a job ad and the app uses GPT OSS 20B (via Groq) to pull out:
- the role and seniority level
- a two-sentence plain-English summary
- must-have and nice-to-have technical skills, with alternatives such as "Python, R or Java" grouped into one item

## How it works

```
Raw job ads (CSV)
  -> clean.py       remove HTML, URLs and boilerplate (salary, benefits, etc.)
  -> skills.py      match about 75 skills using a regex dictionary with aliases
  -> skill_counts   % of ads per job title that mention each skill
  -> app (page 1)   interactive Plotly chart

Pasted job ad
  -> llm.py         GPT OSS 20B with JSON mode, temperature 0, low reasoning effort
  -> validate()     check types, apply defaults, restrict seniority values, remove duplicates
  -> app (page 2)   role, summary and skill badges
```

## Key decisions

- **Rejected a "perfect" dataset.** A 1.1M-row dataset turned out to contain only 269 unique descriptions, so it was synthetic. I used a smaller dataset of real ads instead.
- **Percent of ads, not raw counts.** Each skill is counted once per ad, and ads where no skill was found (116 of 2,275, mostly non-tech listings) are left out of the percentages.
- **Regex with word boundaries.** Lookbehind and lookahead rules stop "Java" matching inside "JavaScript", and "C" matching inside "C++".
- **Never trust raw LLM output.** JSON mode guarantees valid JSON, and a Python validation layer guarantees the right shape.
- **Prompt iteration on real ads.** Testing on live job ads showed the model listing "Python, R or Java" as three separate must-haves, so I changed the prompt to group alternatives.
- **Model migration.** The original model (Llama 3.1 8B Instant) was decommissioned mid-project, so I moved to GPT OSS 20B and set the reasoning effort to low for speed.
- **Cross-platform paths.** Data paths are built with `pathlib` from the module's own location, so the app runs the same on Windows locally and on Linux in the cloud.

## Tech stack

Python, Pandas, regex, Streamlit, Plotly Express, Groq API (GPT OSS 20B), Streamlit Community Cloud

## Run it locally

```bash
git clone https://github.com/nehaanil79/tech-skills-recommender.git
cd tech-skills-recommender
python -m venv venv
venv\Scripts\activate        # Windows (on macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` with your free Groq API key:

```toml
GROQ_API_KEY = "gsk_your_key_here"
```

Then run:

```bash
streamlit run app.py
```

## Limitations

- The dataset is Indian job ads from around 2020–21, so skill demand may differ from today's Australian market.
- The skills dictionary covers about 75 skills, so page 1 can't show skills outside it.
- Broad categories that an ad lists by name (for example "GenAI tools") are extracted as written.

## Future improvements

- Compare AI extraction with the keyword baseline on the same ad (found by both, AI only, keyword only)
- Skill gap analysis: compare your skills with the job's skills, ranked by market demand
- Resume upload to fill in your skills automatically
- Refresh the dataset with recent Australian job ads