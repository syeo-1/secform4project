from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Form_4_data
# from config import *

# Initialize FastAPI
app = FastAPI()

@app.get("/data/")
def get_users(db: Session = Depends(get_db)):
    data = db.query(Form_4_data).all()
    return data

# @app.get('/')

# DATABASE_URL = "postgresql://airflow:airflow@sec_form_data:5432/airflow"
# from sqlalchemy import create_engine

# # DATABASE_URL = "postgresql://airflow:airflow@localhost:5432/airflow"
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:5432/{DB_NAME}"
# engine = create_engine(DATABASE_URL)

