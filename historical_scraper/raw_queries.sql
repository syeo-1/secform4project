-- for detecting duplicates
-- apparently I do not have any duplicates
SELECT
reporting_owner_name,
issuer_name,
ticker_symbol,
acceptance_time,
security_title,
transaction_date,
deemed_execution_date,
transaction_code,
num_transaction_shares,
acquired_or_disposed,
transaction_share_price,
amount_owned_after_transaction,
ownership_form,
original_form_4_text_url,
COUNT(*)
FROM public.form_4_data
GROUP BY
reporting_owner_name,
issuer_name,
ticker_symbol,
acceptance_time,
security_title,
transaction_date,
deemed_execution_date,
transaction_code,
num_transaction_shares,
acquired_or_disposed,
transaction_share_price,
amount_owned_after_transaction,
ownership_form,
original_form_4_text_url
HAVING COUNT(*) > 1;

-- get all data for today from form_4_data table
SELECT *
FROM public.form_4_data
WHERE DATE(acceptance_time) = CURRENT_DATE;