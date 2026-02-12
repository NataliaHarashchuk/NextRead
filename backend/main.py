import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models 

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Отримуємо рядок з .env, якщо його немає — використовуємо порожній список
origins_raw = os.getenv("ALLOWED_ORIGINS", "")

# Розбиваємо рядок по комі, щоб отримати список ["http://...", "http://..."]
origins = [origin.strip() for origin in origins_raw.split(",")] if origins_raw else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {"message": "CORS is configured via .env", "allowed_origins": origins}

@app.get('/items/')
def read_items(db: Session = Depends(get_db)):
    return {"message": "Database session is active"}