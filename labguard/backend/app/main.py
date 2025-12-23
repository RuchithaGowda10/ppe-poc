from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.auth.login import router as login_router
from app.auth.register import router as register_router
from app.lms.trigger import router as lms_router
from app.lms.labs import router as lab_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LabGuard AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://erp.company.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.mount(
    "/snapshots",
    StaticFiles(directory="storage/snapshots"),
    name="snapshots"
)

app.include_router(register_router, prefix="/auth")
app.include_router(login_router, prefix="/auth")
app.include_router(lms_router, prefix="/lms")
app.include_router(lab_router, prefix="/lms")

@app.get("/")
def health():
    return {"status": "LabGuard running"}
