from fastapi import FastAPI
from app.database import Base, engine
from app.routers import findings, dashboard
import time

app = FastAPI(title="Pentzy VA Platform")

@app.on_event("startup")
def startup_event():
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected successfully")
            break
        except Exception as e:
            print("⏳ Waiting for database...")
            retries -= 1
            time.sleep(3)

app.include_router(findings.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Pentzy backend is running"}
