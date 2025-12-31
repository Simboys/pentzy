from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import findings, dashboard, scans
from app.auth import routes as auth_routes
import time

app = FastAPI(title="Pentzy VA Platform")

# ✅ CORS CONFIGURATION (MANDATORY FOR UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.157.146:5173"  # 🔁 replace with YOUR Kali IP
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected successfully")
            break
        except Exception:
            print("⏳ Waiting for database...")
            retries -= 1
            time.sleep(3)

# Routers
app.include_router(auth_routes.router)
app.include_router(findings.router)
app.include_router(dashboard.router)
app.include_router(scans.router)

@app.get("/")
def root():
    return {"message": "Pentzy backend is running"}
