import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# Get Supabase credentials from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

# IMPORTANT: This allows your frontend to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://almanack007.github.io"], # Your live frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "Your FastAPI backend is live!"}

# The API route your frontend is looking for
@app.get("/api/kpis")
def get_kpis():
    # For now, we return DUMMY data to prove it works.
    # Later, you will replace this with a real query to your Supabase database.
    print("KPIs endpoint was called successfully!")
    return {
        "callVolume": 1240,
        "resolutionRate": 0.87,
        "sentiment": { "positive": 0.62, "neutral": 0.28, "negative": 0.10 },
        "jobTypeDistribution": [
            { "type": "Booking", "count": 500 },
            { "type": "Inquiry", "count": 440 },
            { "type": "Support", "count": 200 },
            { "type": "Other", "count": 100 }
        ],
        "trend": [
            { "day": "Mon", "calls": 200 },
            { "day": "Tue", "calls": 220 },
            { "day": "Wed", "calls": 250 },
            { "day": "Thu", "calls": 280 },
            { "day": "Fri", "calls": 260 },
            { "day": "Sat", "calls": 180 },
            { "day": "Sun", "calls": 150 }
        ]
    }
