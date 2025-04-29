
interface TransactionObject {
    reporting_owner_name: string;
    issuer_name: string;
    ticker_symbol: string;
    acceptance_time: string;
    total_filing_transaction_value: number;
    original_form_4_text_url: string;
}

export type { TransactionObject as Transaction }