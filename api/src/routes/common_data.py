from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select, or_, distinct

router = APIRouter()

@router.get(
    '/api/common/search/',
    summary='get back all relevant queries via substring search for things in database'
)
def get_search_data(db: Session = Depends(get_db)):
    '''
    gets unique values from the following columns for the search bar. Not case-sensitive
    
    reporting_owner_name,
    issuer_name,
    ticker_symbol
    '''

    # unique_reporting_owner_query = select(distinct(Form_4_data.reporting_owner_name)).where(Form_4_data.reporting_owner_name.ilike(f'%{query_string}%'))
    # unique_issuer_name_query = select(distinct(Form_4_data.issuer_name)).where(Form_4_data.issuer_name.ilike(f'%{query_string}%'))
    # unique_ticker_symbol_query = select(distinct(Form_4_data.ticker_symbol)).where(Form_4_data.ticker_symbol.ilike(f'%{query_string}%'))
    unique_reporting_owner_query = select(distinct(Form_4_data.reporting_owner_name))
    unique_issuer_name_query = select(distinct(Form_4_data.issuer_name))
    unique_ticker_symbol_query = select(distinct(Form_4_data.ticker_symbol))

    result = set()

    result.update(db.execute(unique_reporting_owner_query).scalars().all())
    result.update(db.execute(unique_issuer_name_query).scalars().all())
    result.update(db.execute(unique_ticker_symbol_query).scalars().all())

    return list(result)

@router.get(
        '/api/common/all_tickers',
        summary='retrieve all ticker symbols used in insider trading from most recent 365 days'
)
def get_all_ticker_symbol_data(db: Session = Depends(get_db)):
    '''
        returns a list of unique ticker symbol strings from insider trading from the
        last 365 days
    '''
    unique_ticker_symbol_query = select(distinct(Form_4_data.ticker_symbol))

    result = set()

    result.update(db.execute(unique_ticker_symbol_query).scalars().all())
    
    return list(result)


@router.get(
        '/api/common/transaction/{data:path}',
        name="path-converter",
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