'''gives back the top ten largest purchases for a given time period from form 4 data'''
from fastapi import APIRouter, Depends
from ..models import Form_4_data
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select, or_, func, distinct, desc
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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
        '/api/common/top_filings',
        summary='get top 10 data by sale price (no time interval as of yet)'
    )
def get_top_ten_sale_filings(time_interval, transaction_type, db: Session = Depends(get_db)):
    '''get top 10 sale filing data'''

    oldest_allowable_data_iso = None

    eastern = ZoneInfo("America/New_York")
    now_et = datetime.now(eastern)


    match time_interval:
        case 'Day':
            oldest_allowable_data = now_et - timedelta(days=1)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()
        case 'Week':
            oldest_allowable_data = now_et - timedelta(days=7)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()
        case 'Month':
            oldest_allowable_data = now_et - timedelta(days=30)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()
        case 'Year':
            oldest_allowable_data = now_et - timedelta(days=365)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()

    query = select(
        Form_4_data.reporting_owner_name,
        Form_4_data.issuer_name,
        Form_4_data.ticker_symbol,
        Form_4_data.acceptance_time,
        func.sum(Form_4_data.num_transaction_shares * Form_4_data.transaction_share_price).label("total_filing_transaction_value"),
        Form_4_data.original_form_4_text_url
    ).where(
        Form_4_data.transaction_code == transaction_type,
        Form_4_data.transaction_share_price.isnot(None),
        Form_4_data.acceptance_time >= oldest_allowable_data_iso
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


@router.get(
        '/api/common/top_activity',
        summary='get top 10 data by sale price (no time interval as of yet)'
    )
def get_top_ten_activity_filings(time_interval, db: Session = Depends(get_db)):
    '''
        get top 10 activity company data

        ie. within a given timeframe, see which companies have had the most activity total

        (the greatest number of sales and purchases in the given timeframe)
    '''

    oldest_allowable_data_iso = None

    eastern = ZoneInfo("America/New_York")
    now_et = datetime.now(eastern)


    match time_interval:
        case 'Day':
            oldest_allowable_data = now_et - timedelta(days=1)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()
        case 'Week':
            oldest_allowable_data = now_et - timedelta(days=7)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()
        case 'Month':
            oldest_allowable_data = now_et - timedelta(days=30)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()
        case 'Year':
            oldest_allowable_data = now_et - timedelta(days=365)
            oldest_allowable_data_iso = oldest_allowable_data.isoformat()

    # first, get the top ten tickers with the most transactions by counting the
    # number of rows and getting the top ten highest count

    frequency = func.count(Form_4_data.ticker_symbol).label('frequency')

    query = select(
        
            Form_4_data.ticker_symbol,
            frequency
        
    ).where(
        Form_4_data.transaction_share_price.isnot(None),
        Form_4_data.acceptance_time >= oldest_allowable_data_iso
    ).group_by(
        Form_4_data.ticker_symbol,
    ).order_by(
        desc(frequency)
    ).limit(10)

    top_tickers = db.execute(query).scalars().all()

    return top_tickers 