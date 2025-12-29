import os
from app.routes.sdk_ingest import router as sdk_router
from app.routes.sdk_commands import router as sdk_cmd_router
from app.routes.sdk_ingest import router as sdk_ingest_router
from app.lms.entry_status import router as entry_status_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.lms.trigger import router as lms_router
from app.lms.labs import router as lab_router

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
    allow_headers=["Authorization", "Content-Type", "X-User-Id", "X-User-Email"],
)

# ============================
# SNAPSHOT STORAGE (SAFE)
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
app.include_router(lms_router, prefix="/lms")
app.include_router(lab_router, prefix="/lms")
app.include_router(sdk_router)
app.include_router(sdk_cmd_router)
app.include_router(sdk_ingest_router)
app.include_router(entry_status_router, prefix="/lms")

# ============================
# HEALTH
# ============================
@app.get("/")
def health():
    return {"status": "LabGuard running"}
