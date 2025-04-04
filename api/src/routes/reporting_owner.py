'''endpoints for retrieving data related to the transaction reporting owner'''
from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select

router = APIRouter()

@router.get(
        '/reporting_owner/{reporting_owner}',
        summary='Get Transaction Related to a Specific Individual'
    )
def get_reporting_owner_data(reporting_owner: str, db: Session = Depends(get_db)):
    '''get transactions related to a specific individual'''
    query_statement = select(Form_4_data).where(Form_4_data.reporting_owner_name == reporting_owner)
    result = db.execute(query_statement)
    data = result.scalars().all()

    return data