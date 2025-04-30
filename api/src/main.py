from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Form_4_data
from .routes import company_name, reporting_owner, ticker, top_data, common_data
from fastapi.middleware.cors import CORSMiddleware
# from config import *

# Initialize FastAPI
app = FastAPI(redirect_slashes=True)

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_name.router)
app.include_router(reporting_owner.router)
app.include_router(ticker.router)
app.include_router(top_data.router)
app.include_router(common_data.router)

# @app.get("/data/")
# def get_users(db: Session = Depends(get_db)):
#     data = db.query(Form_4_data).all()
#     return data

# @app.get('/')

# DATABASE_URL = "postgresql://airflow:airflow@sec_form_data:5432/airflow"
# from sqlalchemy import create_engine

# # DATABASE_URL = "postgresql://airflow:airflow@localhost:5432/airflow"
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:5432/{DB_NAME}"
# engine = create_engine(DATABASE_URL)

