import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# Get Supabase credentials from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

# This allows your frontend to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "Your FastAPI backend is live and running!"}

# The API route for the Dashboard tab
@app.get("/api/kpis")
def get_kpis():
    print("KPIs endpoint was called successfully!")
    # For now, we return DUMMY data. Later, you will replace this with a real query.
    return {
        "callVolume": 1240,
        "resolutionRate": 0.87,
        "sentiment": { "positive": 0.62, "neutral": 0.28, "negative": 0.10 },
        "jobTypeDistribution": [
            { "type": "Booking", "count": 500 }, { "type": "Inquiry", "count": 440 },
            { "type": "Support", "count": 200 }, { "type": "Other", "count": 100 }
        ],
        "trend": [
            { "day": "Mon", "calls": 200 }, { "day": "Tue", "calls": 220 },
            { "day": "Wed", "calls": 250 }, { "day": "Thu", "calls": 280 },
            { "day": "Fri", "calls": 260 }, { "day": "Sat", "calls": 180 }, { "day": "Sun", "calls": 150 }
        ]
    }

# The API route for the Call Records tab
@app.get("/api/calls")
def get_calls():
    print("Calls endpoint was called successfully!")
    # Dummy data: an empty list of items
    return {"items": []}

# --- ADDING THE MISSING ROUTES BELOW ---

@app.get("/api/service-insights")
def get_service_insights():
    print("Service Insights endpoint called")
    # Dummy data
    return {"categories": []}

@app.get("/api/summaries")
def get_summaries():
    print("Summaries endpoint called")
    # Dummy data
    return {"items": []}

@app.get("/api/integrations")
def get_integrations():
    print("Integrations endpoint called")
    # Dummy data
    return {"items": []}

@app.get("/api/settings")
def get_settings():
    print("Settings endpoint called")
    # Dummy data
    return {"security": {}, "dataRetention": {}, "accessControls": {"roles": []}}
