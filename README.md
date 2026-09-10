# 🌟 AI Job Mentor for Informal Workers

> **Powered by IBM Granite via watsonx.ai · Multi-Agent RAG Architecture**

An AI-powered career guidance application designed to help India's 450M+ informal workers find better jobs, bridge skill gaps, access government welfare schemes, and grow their careers — available in **English**, **हिंदी (Hindi)**, and **தமிழ் (Tamil)**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 👤 **Worker Profile** | Build a rich profile with skills, education, income, and language preferences |
| 💼 **Job Recommendations** | AI-scored job matches with breakdown by skill, education, experience & salary |
| 📊 **Skill Gap Analysis** | Visual analysis of what skills you have vs. what target jobs require |
| 🎓 **Training Recommendations** | Government & private training programmes ranked by relevance and cost |
| 🏛️ **Government Schemes** | Automatic eligibility check for PM-SYM, ESIC, BOCW, e-Shram, and more |
| 🤖 **AI Mentor Chat** | Multi-turn conversational mentor "Aasha" powered by IBM Granite |
| 🌐 **3 Languages** | Full UI and AI responses in English, Hindi, and Tamil |
| 🔄 **Demo Mode** | 5 pre-built worker profiles with realistic data — works offline |

---

## 🏗️ Architecture

```
AI_Job_Mentor_IBM/
├── app.py                   # Streamlit multi-section UI
├── watsonx_client.py        # IBM Granite API client + fallback
├── rag_engine.py            # TF-IDF RAG retrieval engine
├── agents/
│   ├── job_agent.py         # Job matching & recommendation
│   ├── skill_agent.py       # Skill gap analysis
│   ├── training_agent.py    # Training programme matching
│   ├── scheme_agent.py      # Government scheme eligibility
│   └── mentor_agent.py      # Conversational AI mentor (Aasha)
├── data/
│   └── demo_data.py         # Jobs, training, schemes, worker profiles
├── i18n/
│   └── translations.py      # English / Hindi / Tamil strings
├── .env.example             # Environment variable template
├── requirements.txt
└── README.md
```

### Multi-Agent Flow

```
User Input
    │
    ▼
[Streamlit UI]  ──language switch──▶  [i18n / Translations]
    │
    ├──▶ [Job Agent]       → match scores + IBM Granite narrative
    ├──▶ [Skill Agent]     → gap analysis + IBM Granite analysis
    ├──▶ [Training Agent]  → programme ranking + IBM Granite guidance
    ├──▶ [Scheme Agent]    → eligibility check + IBM Granite guidance
    └──▶ [Mentor Agent]    → multi-turn chat (Aasha) + IBM Granite
              │
              ▼
        [RAG Engine]  ──retrieves context──▶  [IBM Granite via watsonx.ai]
```

---

## 🚀 Quick Start

### 1. Clone / Download

```bash
git clone https://github.com/your-org/AI_Job_Mentor_IBM.git
cd AI_Job_Mentor_IBM
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your IBM watsonx.ai credentials
```

**`.env` contents:**

```env
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_MODEL_ID=ibm/granite-4-h-small
```

> **No API key?** The app runs in **offline/demo mode** automatically — all features work with pre-built responses.

### 4. Run the App

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🔑 IBM watsonx.ai Configuration

| Variable | Description | Default |
|---|---|---|
| `WATSONX_API_KEY` | IBM Cloud API key | *(required for live AI)* |
| `WATSONX_URL` | watsonx.ai generation endpoint | us-south endpoint |
| `WATSONX_PROJECT_ID` | Your watsonx.ai project ID | *(required for live AI)* |
| `WATSONX_MODEL_ID` | Model to use | `ibm/granite-4-h-small` |

Get your credentials at [IBM watsonx.ai](https://dataplatform.cloud.ibm.com/).

---

## 👤 Demo Profiles

| ID | Name | Occupation | Location |
|---|---|---|---|
| W001 | Ramesh Kumar | Construction Labour | Chennai, TN |
| W002 | Meena Devi | Domestic Worker | Patna, Bihar |
| W003 | Suresh Babu | Street Vendor | Mumbai, MH |
| W004 | Lakshmi S | Garment Worker | Coimbatore, TN |
| W005 | Arjun Singh | Delivery Boy | Delhi |

---

## 🧠 RAG (Retrieval-Augmented Generation)

The app uses a lightweight in-memory RAG engine:

1. **Corpus**: All job listings, training programmes, and government schemes are indexed.
2. **Retrieval**: TF-IDF cosine similarity finds the most relevant 3–4 documents for each query.
3. **Augmentation**: Retrieved context is prepended to the IBM Granite prompt.
4. **Generation**: IBM Granite produces grounded, factual responses.

No external vector database is required — everything runs in-process.

---

## 🏛️ Government Schemes Covered

- **PM-SYM** — Pension for informal workers
- **ESIC** — Health insurance
- **PMJDY** — Zero-balance bank account
- **PMJJBY** — Life insurance (₹2L cover at ₹436/yr)
- **PMSBY** — Accident insurance (₹2L at ₹20/yr)
- **BOCW** — Construction worker welfare
- **e-Shram** — Unique worker identity card
- **Sukanya Samriddhi** — Girl child savings

---

## 📦 Dependencies

```
streamlit         — UI framework
requests          — IBM watsonx.ai API calls
python-dotenv     — Environment variable loading
numpy / pandas    — Data processing
scikit-learn      — (available for future ML features)
Pillow            — Image handling
```

---

## 🛡️ Offline / Fallback Mode

If `WATSONX_API_KEY` is not set or the API is unavailable:
- All matching algorithms (job scores, skill gaps, scheme eligibility) run **fully locally**.
- AI narrative sections show pre-written, domain-appropriate fallback responses.
- A yellow banner clearly indicates offline mode to the user.

---

## 📄 License

MIT License — Free to use, modify, and distribute.

---

*Built with ❤️ for India's informal workforce · IBM watsonx.ai Hackathon*
