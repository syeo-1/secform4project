'''endpoints for retrieving data related to the transaction reporting owner'''
from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/reporting_owner/")
def get_users(db: Session = Depends(get_db)):
    data = db.query(Form_4_data).all()
    return data

# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}