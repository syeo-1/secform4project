import psycopg2
from datetime import datetime
from pytz import timezone
from pprint import pformat
import logging
import os

FORM_4_TABLE_DROP = '''
    DROP TABLE IF EXISTS
    form_4_data;
'''

FORM_4_TABLE_STATEMENT = '''
    CREATE TABLE IF NOT EXISTS
    form_4_data
    (
    form_4_id SERIAL,
    reporting_owner_name TEXT,
    issuer_name TEXT,
    ticker_symbol TEXT,
    acceptance_time TIMESTAMP NULL,
    security_title TEXT,
    transaction_date TIMESTAMPTZ,
    deemed_execution_date DATE,
    transaction_code TEXT,
    num_transaction_shares INTEGER,
    acquired_or_disposed TEXT,
    transaction_share_price NUMERIC(15,4),
    amount_owned_after_transaction TEXT,
    ownership_form TEXT,
    original_form_4_text_url TEXT,
    PRIMARY KEY(acceptance_time, reporting_owner_name, ticker_symbol, amount_owned_after_transaction),
    CONSTRAINT form_4_constraint UNIQUE (acceptance_time, reporting_owner_name, ticker_symbol, amount_owned_after_transaction)
    );
'''

def upload_form_4_data(db_user, db_name, db_password, host, form_4_data, daily_unneeded_links):
    '''take a db connection and upload the form 4 data to the appropriate table'''

    table_name = 'form_4_data'
    columns = f'''
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
    '''

    connection = psycopg2.connect(f'dbname={db_name} user={db_user} password={db_password} host={host}')
    cursor = connection.cursor()

    # insertion_issue_data = []
    form_4_filing_set = set()
    # tz = timezone('US/Eastern')
    # data.append(str(datetime.now(tz)))

    # try:
    #     cursor.execute(FORM_4_TABLE_DROP)
    #     print('form 4 table dropped')
    # except Exception as e:
    #     print(e)

    try:
        cursor.execute(FORM_4_TABLE_STATEMENT)
        print('Form 4 table successfully generated')
    except psycopg2.Error as postgres_table_creation_error:
        print(f'Error in generating form 4 table in postgres: {postgres_table_creation_error}')

    # print(data)
    # print(columns)
    # print(table_name)
    for data in form_4_data:
        # TODO: need to figure out how to handle following error:
        # INFO - error in inserting form 4 data into postgres table: current transaction is aborted, commands ignored until end of transaction block
        logging.info(f'data value is: {data}')
        try:
            cursor.execute(f'''
                INSERT INTO {table_name}({columns}) values(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                ) ON CONFLICT (acceptance_time, reporting_owner_name, ticker_symbol, amount_owned_after_transaction) DO NOTHING
            ''', tuple(data.values()))
            if cursor.rowcount != 1:
                print(f'data already exists in db or some other issue occured: {data.values()}')
                # insertion_issue_data.append(data['original_form_4_text_url'])
                form_4_filing_set.add(data['original_form_4_text_url'])
            elif cursor.rowcount == 1:
                form_4_filing_set.add(data['original_form_4_text_url'])
        except psycopg2.Error as postgres_insert_error:
            print(f'error in inserting form 4 data into postgres table: {postgres_insert_error}')
        except ValueError as value_error:
            print(f'value error occured: {value_error}')
        except TypeError as type_error:
            print(f'type error occured: {type_error}')
        except Exception as e:
            print(f'general error occured: {e}')
    
        connection.commit()

    connection.close()
    cursor.close()

    # print(insertion_issue_data)

    # ensure that the set has all the data
    set_with_all_used_links = daily_unneeded_links.union(form_4_filing_set)

    # check if the daily temp data file already exists. If it doesn't, create it
    # if it does exist, overwrite with the combination of the new and the old data
    filename = 'temp_daily_data_links.txt'
    # filename2 = 'data_links_with_issues.txt'
    # if os.path.exists(filename) and os.path.isfile(filename):
    #     # file already exists, overwrite with combination of old and new data links
    #     with open(filename, 'w') as f:
    #         for link in set_with_all_used_links:
    #             f.write(f'{link}\n')
    # elif not os.path.exists(filename):
    #     # file does not exist yet, so create it and write to it!
    with open(filename, 'w') as f:
        for link in set_with_all_used_links:
            f.write(f'{link}\n')
    # with open(filename2, 'w') as f:
    #     for link in insertion_issue_data:
    #         f.write(f'{link}\n')


if __name__ == '__main__':
    test_data = ['11084', 'D', 'Workday, Inc.', 'WDAY', '253.63', '2025-03-05', '20250307182858']






