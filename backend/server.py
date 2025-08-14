import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Optional Mongo (not required for scaffold); we only connect if MONGO_URL exists
try:
    from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
except Exception:  # pragma: no cover
    AsyncIOMotorClient = None  # type: ignore

app = FastAPI(title="Voice Agenda Platform API", openapi_url="/api/openapi.json")

# CORS - keep permissive for scaffold; ingress handles external routing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    mongo_url = os.environ.get("MONGO_URL")
    if mongo_url and AsyncIOMotorClient is not None:
        try:
            client = AsyncIOMotorClient(mongo_url)
            app.state.mongo_client = client
            app.state.db = client.get_default_database()
        except Exception as e:  # pragma: no cover
            # Log-only; app continues with in-memory data
            print(f"[startup] Mongo connection failed: {e}")
    else:
        print("[startup] MONGO_URL not set or motor not installed; running without DB")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    client = getattr(app.state, "mongo_client", None)
    if client is not None:
        client.close()


# ------- Helpers (stub data generation) -------

def _uuid() -> str:
    return str(uuid.uuid4())


def _iso(dt: datetime) -> str:
    return dt.isoformat()


# ------- API Routes (all prefixed with /api) -------

@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/kpis")
async def get_kpis():
    return {
        "callVolume": 1240,
        "resolutionRate": 0.87,
        "sentiment": {"positive": 0.62, "neutral": 0.28, "negative": 0.10},
        "jobTypeDistribution": [
            {"type": "Domestic Job Requests", "count": 520, "color": "#4CAF50"},
            {"type": "Technical Support", "count": 420, "color": "#8BC34A"},
            {"type": "Billing", "count": 180, "color": "#A5D6A7"},
            {"type": "Other", "count": 120, "color": "#C8E6C9"},
        ],
        "trend": [
            {"day": "Mon", "calls": 180},
            {"day": "Tue", "calls": 200},
            {"day": "Wed", "calls": 220},
            {"day": "Thu", "calls": 280},
            {"day": "Fri", "calls": 260},
            {"day": "Sat", "calls": 160},
            {"day": "Sun", "calls": 140},
        ],
    }


@app.get("/api/calls")
async def get_calls():
    now = datetime.utcnow()
    records = []
    base = [
        ("Alex Johnson", "Domestic Job Request", "positive", "Resolved"),
        ("Priya Shah", "Technical Support", "neutral", "Pending"),
        ("Miguel Diaz", "Billing", "negative", "Escalated"),
        ("Sara Lee", "Domestic Job Request", "positive", "Resolved"),
        ("Noah Chen", "Technical Support", "neutral", "Resolved"),
        ("Emma Brown", "Other", "positive", "Resolved"),
    ]
    for i, (name, ctype, sentiment, status) in enumerate(base):
        records.append(
            {
                "id": _uuid(),
                "callerName": name,
                "callType": ctype,
                "datetime": _iso(now - timedelta(hours=i * 3 + 1)),
                "sentiment": sentiment,
                "resolutionStatus": status,
            }
        )
    return {"items": records}


@app.get("/api/service-insights")
async def service_insights():
    return {
        "categories": [
            {
                "name": "Domestic Job Requests",
                "count": 520,
                "avgHandleTime": 6.2,
                "firstCallResolution": 0.78,
            },
            {
                "name": "Technical Support",
                "count": 420,
                "avgHandleTime": 9.1,
                "firstCallResolution": 0.62,
            },
            {
                "name": "Billing",
                "count": 180,
                "avgHandleTime": 4.8,
                "firstCallResolution": 0.81,
            },
        ]
    }


@app.get("/api/summaries")
async def summaries():
    return {
        "items": [
            {
                "id": _uuid(),
                "caller": "Alex Johnson",
                "transcriptPreview": "Hi, I need to schedule a domestic cleaning job for next week...",
                "actionItems": ["Assign to field team", "Confirm schedule", "Send confirmation"],
            },
            {
                "id": _uuid(),
                "caller": "Priya Shah",
                "transcriptPreview": "My Wi‑Fi keeps dropping; can someone troubleshoot remotely?",
                "actionItems": ["Open support ticket", "Assign L2 engineer"],
            },
            {
                "id": _uuid(),
                "caller": "Miguel Diaz",
                "transcriptPreview": "I was overcharged on my last invoice and need a refund review...",
                "actionItems": ["Escalate to billing", "Notify customer"],
            },
        ]
    }


@app.get("/api/integrations")
async def integrations():
    return {
        "items": [
            {"name": "CRM", "enabled": True},
            {"name": "Ticketing", "enabled": False},
            {"name": "Scheduling", "enabled": True},
            {"name": "Slack", "enabled": False},
        ]
    }


@app.get("/api/settings")
async def settings():
    return {
        "security": {"mfa": True, "sso": True, "ipAllowlist": False},
        "dataRetention": {"transcriptsDays": 365, "analyticsMonths": 24},
        "accessControls": {"roles": ["Admin", "Manager", "Agent"], "defaultRole": "Agent"},
    }