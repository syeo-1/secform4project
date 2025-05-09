
interface TransactionObject {
    reporting_owner_name: string;
    issuer_name: string;
    ticker_symbol: string;
    acceptance_time: string;
    total_filing_transaction_value: number;
    original_form_4_text_url: string;
    transaction_code: string;
    num_transaction_shares: number;
    form_4_id: number;
    transaction_share_price: number;
}

export type { TransactionObject as Transaction }