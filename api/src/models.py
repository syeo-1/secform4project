from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, Numeric
from .database import Base

class Form_4_data(Base):
    __tablename__ = "form_4_data"  # Must match your actual table name in PostgreSQL

    form_4_id = Column(Integer, primary_key=True, index=True)
    reporting_owner_name = Column(String, index=True)
    issuer_name = Column(String, unique=False, index=True)
    ticker_symbol = Column(String, unique=False, index=True)
    acceptance_time = Column(TIMESTAMP, unique=False, index=True) 
    security_title = Column(String, unique=False, index=True)
    transaction_date = Column(TIMESTAMP, unique=False, index=True)
    deemed_execution_date = Column(DateTime, index=True) 
    transaction_code = Column(String, unique=False, index=True)
    num_transaction_shares = Column(Integer, unique=False, index=True)
    acquired_or_disposed = Column(String, unique=False, index=True)
    transaction_share_price = Column(Numeric, unique=False, index=True)
    amount_owned_after_transaction = Column(String, unique=False, index=True)
    ownership_form = Column(String, unique=False, index=True)
    original_form_4_text_url = Column(String, unique=False, index=True)

