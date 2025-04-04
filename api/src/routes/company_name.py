
from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select

router = APIRouter()

@router.get(
        '/company_name/{company_name}',
        summary='Get Transaction Related to a Specific Company Name'
    )
def get_company_name_data(company_name: str, db: Session = Depends(get_db)):
    '''get transactions related to a specific company name'''
    query_statement = select(Form_4_data).where(Form_4_data.issuer_name == company_name)
    result = db.execute(query_statement)
    data = result.scalars().all()

    return data