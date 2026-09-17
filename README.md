# 🤖 TheButler — AI Agent for Data Analyst Internships

**TheButler** is a production-quality, autonomous **AI internship discovery and application agent** designed specifically for Computer Science students seeking **Data Analyst / Data Analytics internships**, with a strong focus on **Remote / Work From Home opportunities in India**.

---

## 🌟 Key Features

1. **Multi-Source Job Discovery (8 Sources):**
   - LinkedIn Jobs, Naukri, Indeed, Internshala, Wellfound, Glassdoor, Foundit, Cutshort + direct career pages.
2. **Deduplication Engine:**
   - Groups identical listings across multiple job portals into a single canonical job card.
3. **Fraud & Scam Detection:**
   - Detects upfront payment demands ("registration fee", "training fee"), suspicious domains, and Telegram/WhatsApp recruitment scams. Automatically flags and excludes malicious listings.
4. **Transparent Multi-Factor Job Matching:**
   - Evaluates jobs across 7 criteria: Role Match (20%), Skill Match (30%), Experience Match (15%), Education Match (10%), Location Match (5%), Remote Preference (10%), and Project Relevance (10%).
5. **Factual AI Resume Tailoring:**
   - Re-weights skill sections and prioritizes relevant projects (e.g. *SkyMetrics*, *DataflowX*, *Netflix Dashboard*) without fabricating experience or qualifications.
6. **Factual Application QA Generation:**
   - Generates truthful answers for common application questions based strictly on verified student profile facts. Flags sensitive/legal questions for human review.
7. **Human Approval Workflow (`APPROVAL_REQUIRED` Mode):**
   - Mandates explicit user approval (`[APPROVE & SUBMIT]`) before submitting any application.
8. **Playwright Automation & Compliance Halts:**
   - Auto-fills permitted form fields via Playwright and gracefully halts on CAPTCHA, login walls, or security checks, offering a 1-click manual handoff card.
9. **Interactive Streamlit Dashboard:**
   - First-run Onboarding setup wizard, Overview analytics, Filterable Job Feed, Application Kanban board, Profile & Master Resume editor, and System Settings.

---

## 🏗️ Architecture

```text
TheButler/
├── app/
│   ├── main.py                    # FastAPI server entry point
│   ├── config.py                  # Pydantic Settings
│   ├── agents/                    # Job Discovery, Matcher, Fraud Detector, Resume/App Agents
│   ├── sources/                   # 8 Modular Job Source fetchers (LinkedIn, Naukri, Indeed, etc.)
│   ├── browser/                   # Playwright automation manager & application runner
│   ├── database/                  # SQLAlchemy models & SQLite/Postgres DB setup
│   ├── resume/                    # Resume parser, tailor, and generator
│   └── services/                  # Deduplication, APScheduler, Notification services
├── dashboard/
│   ├── app.py                     # Streamlit entry point
│   └── pages/                     # Onboarding, Dashboard, Job Feed, Kanban, Profile, Settings
├── tests/                         # Pytest test suite
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/Hameeem/TheButler.git
cd TheButler

python -m venv venv
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

### 2. Launch FastAPI Backend

```bash
uvicorn app.main:app --reload
```
API documentation available at: `http://localhost:8000/docs`

### 3. Launch Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```
Open your browser at: `http://localhost:8501`

### 4. Run Test Suite

```bash
python -m pytest tests/
```

---

## 🛡️ Compliance & Safety Rules

- Respects website terms of service and rate limits.
- Halts immediately on CAPTCHA, OTP, login prompts, or payment requests.
- Never fabricates qualifications, work experience, or certifications.
- Never submits applications without explicit user approval by default.

---

## 📜 License

MIT License. Designed for AI-powered career automation.
