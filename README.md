```
talentscout-agent/
├── backend/
│   ├── main.py          # FastAPI entry point
│   ├── agent.py         # LangGraph logic & State definition
│   ├── database.py      # PostgreSQL connection (Supabase/Neon)
│   └── schemas.py       # Pydantic models for data extraction
├── frontend/
│   └── app.py           # Streamlit UI
├── .env                 # API Keys (GROQ_API_KEY, DATABASE_URL)
└── requirements.txt
```
