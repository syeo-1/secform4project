'''endpoints for retrieving data related to the stock ticker symbol'''
from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select

router = APIRouter()

@router.get(
        '/api/ticker/{ticker}',
        summary='Get Transactions for Ticker',
    )
def get_ticker_data(ticker: str, db: Session = Depends(get_db)):
    '''get transactions related to a specific ticker symbol'''
    query_statement = select(Form_4_data).where(Form_4_data.ticker_symbol == ticker)
    result = db.execute(query_statement)
    data = result.scalars().all()

    return data
