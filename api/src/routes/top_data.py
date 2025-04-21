'''gives back the top ten largest purchases for a given time period from form 4 data'''
from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select, or_, func, distinct

router = APIRouter()

'''
 lay out the query I want to do:

 - for example, I want the top 10 sales by value of a given day
 - one form can be associated with several specific sales or orders,
    however, the plan will be to group these transactions together by 
        - reporting_owner_name, issuer_name, ticker_symbol, and acceptance time
        since one form can have several transactions, but they will be part of the same form
        - uhh, maybe just group them by the form url then, since the form url will be unique

    - on grouping them in the same url, get the reporting_name, issuer_name, ticker_symbol and acceptance_time
    - at the same time, sum up the product of the grouped transactions of the number of shares multiplied by the specific share price

select reporting_owner_name, issuer_name, ticker_symbol, acceptance_time, sum(num_transaction_shares*transaction_share_price) as total_filing_transaction_value, original_form_4_text_url from public.form_4_data
where transaction_code='S' and transaction_share_price is not null
group by reporting_owner_name, issuer_name, ticker_symbol, acceptance_time, original_form_4_text_url, original_form_4_text_url
order by total_filing_transaction_value DESC
limit 10;

'''

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


@router.get(
        '/api/common/top_sale_filings/',
        summary='get top 10 data by sale price (no time interval as of yet)'
    )
def get_top_ten_sale_filings(db: Session = Depends(get_db)):
    '''get top 10 sale filing data'''

    query = select(
        Form_4_data.reporting_owner_name,
        Form_4_data.issuer_name,
        Form_4_data.ticker_symbol,
        Form_4_data.acceptance_time,
        func.sum(Form_4_data.num_transaction_shares * Form_4_data.transaction_share_price).label("total_filing_transaction_value"),
        Form_4_data.original_form_4_text_url
    ).where(
        Form_4_data.transaction_code == 'S',
        Form_4_data.transaction_share_price.isnot(None)
    ).group_by(
        Form_4_data.reporting_owner_name,
        Form_4_data.issuer_name,
        Form_4_data.ticker_symbol,
        Form_4_data.acceptance_time,
        Form_4_data.original_form_4_text_url
    ).order_by(
        func.sum(Form_4_data.num_transaction_shares * Form_4_data.transaction_share_price).desc()
    ).limit(10)

    result = db.execute(query).all()

    column_names = [
        "reporting_owner_name",
        "issuer_name",
        "ticker_symbol",
        "acceptance_time",
        "total_filing_transaction_value",
        "original_form_4_text_url"
    ]
    data = [dict(zip(column_names, row)) for row in result]
    

    return data