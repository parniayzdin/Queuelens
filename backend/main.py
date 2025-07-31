from dotenv import load_dotenv
import os
import traceback
from datetime import datetime, timedelta
from geopy import Nominatim
from fastapi import FastAPI
from sqlalchemy import func 
from fastapi import HTTPException
from geopy.exc import GeocoderTimedOut

from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, select, create_engine
from fastapi.middleware.cors import CORSMiddleware


load_dotenv() #loads my .env file
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True) #created a database connection engine using that URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Report(SQLModel, table =True):
     #connect python to Databases
    id: int | None =Field(default = None, primary_key=True)
    Name: str |None=None
    lat: float
    lon: float
    wait_minutes: int
    created_at: datetime = Field(default_factory=datetime.utcnow) #This records when the report was created, using the current UTC time.
    ttl_minutes: int = 60 #how long the report is valid

@app.on_event("startup")
def startup(): #once the app is running, make the tables (reports)
    SQLModel.metadata.create_all(engine)

@app.post("/reports/") #POST: create something new
def create_report(report: Report):
    with Session(engine) as session:
        session.add(report)
        session.commit()
        session.refresh(report)
        return report
@app.get("/reports/") #retrieve data, and to keep track of valid reports
def read_reports():
    now=datetime.utcnow() #this gets the current time
    with Session(engine) as session:
        statment = select(Report)
        results = session.exec(statment).all() #gets all reports from the atabse
    
        valid_reports = []
        for report in results:
            expiry = report.created_at + timedelta(minutes=report.ttl_minutes)
            if expiry > now:
                valid_reports.append(report)
        return valid_reports

@app.get("/") #examle root route, to see if it works
def read_root():
    return{"message": "QueueLens backend is running!"}
@app.on_event("startup")
def on_startup():
    # WARNING: drops existing tables!
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

#Reports search
geocoder = Nominatim(user_agent="queuelens")


@app.get("/reports/search")
def search(query: str):
    try: #To catch error 
        location = geocoder.geocode(query, timeout=10)
    except GeocoderTimedOut:
        raise HTTPException(504, detail="Geocoding service timed out, please try again later.")
    except Exception as e:
        raise HTTPException(502, detail=f"Geocoding error: {e}")

    if not location:
        raise HTTPException(404, detail="Place not found")

    lat, lon = location.latitude, location.longitude
    radius = 0.005
    now = datetime.utcnow()

    with Session(engine) as session:
        reports = session.exec(
            select(Report)
            .where(func.abs(Report.lat - lat) < radius)
            .where(func.abs(Report.lon - lon) < radius)
        ).all()

    valid = [
        r for r in reports
        if r.created_at + timedelta(minutes=r.ttl_minutes) > now
    ]

    def weight(r):
        age_min = (now - r.created_at).total_seconds() / 60
        return max(0.1, 1 - age_min / r.ttl_minutes)

    avg_wait = None
    if valid:
        ws = [weight(r) for r in valid]
        avg_wait = sum(r.wait_minutes * w for r, w in zip(valid, ws)) / sum(ws)

    return {
        "query": query,
        "lat": lat,
        "lon": lon,
        "avg_wait": avg_wait,
        "reports": valid,
    }