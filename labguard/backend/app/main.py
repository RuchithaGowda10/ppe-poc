import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# LMS routers
from app.lms.trigger import router as trigger_router
from app.lms.labs import router as lab_router
from app.lms.entry_result import router as entry_result_router

# SDK routers
from app.sdk.commands import router as sdk_commands_router
from app.sdk.ingest import router as sdk_ingest_router

load_dotenv()

app = FastAPI(title="LabGuard AI")

# ============================
# CORS
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://erp.company.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-User-Id", "X-User-Email", "X-API-Key"],
)

# ============================
# SNAPSHOT STORAGE
# ============================
SNAPSHOT_DIR = "app/storage/snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

app.mount(
    "/snapshots",
    StaticFiles(directory=SNAPSHOT_DIR),
    name="snapshots"
)

# ============================
# ROUTERS
# ============================

# User / LMS
app.include_router(trigger_router, prefix="/lms")
app.include_router(lab_router, prefix="/lms")
app.include_router(entry_result_router, prefix="/lms")

# SDK (edge agents)
app.include_router(sdk_commands_router, prefix="/sdk")
app.include_router(sdk_ingest_router, prefix="/sdk")

# ============================
# HEALTH
# ============================
@app.get("/")
def health():
    return {"status": "LabGuard running"}
