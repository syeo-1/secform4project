from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select, or_

router = APIRouter()

@router.get(
        '/api/common/{data}',
        summary='Get Transaction Related to a Specific Company Name'
    )
def get_company_name_data(data: str, db: Session = Depends(get_db)):
    '''get transactions related to piece of common data'''

    # check if data is in any one of the given columns
    query_statement = select(Form_4_data).where(
            or_(
                Form_4_data.issuer_name == data,
                Form_4_data.reporting_owner_name == data,
                Form_4_data.ticker_symbol == data
            )
        )
    result = db.execute(query_statement)
    data = result.scalars().all()

    return data