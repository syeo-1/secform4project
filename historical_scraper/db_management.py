'''
some functions to see if some stuff works when saving and removing data from the transaction database
'''

from config import *
import psycopg2
from collections import Counter
from datetime import datetime, timedelta, timezone
from decimal import Decimal

TEST_DATA = [{
    'reporting_owner_name': 'Sean Yeo',
    'issuer_name': 'AKGOWEIANGAW',
    'ticker_symbol': 'AGWENGAKWGANW',
    'acceptance_time': datetime(2024, 6, 3, 16, 58, 46),
    'security_title': 'class C Uncommon 4 stock',
    'transaction_date': datetime(2024, 5, 30, 0, 0, tzinfo=timezone(timedelta(days=-1, seconds=61200))),
    'deemed_execution_date': '2024-11-14 18:43:14',
    'transaction_code': 'S',
    'num_transaction_shares': 43,
    'acquired_or_disposed': 'D',
    'transaction_share_price': 87.23,
    'amount_owned_after_transaction': '4000',
    'ownership_form': 'D',
    'original_form_4_text_url': 'https://google.com',
}]

FORM_4_ALL_ROWS_STATEMENT = '''
SELECT * FROM form_4_data;
'''

def duplicate_transaction_exists():
    '''
        check for duplicate rows in the given database table

        not inclusive of the pid column, check if the same row exists

        if it does exist, return True, otherwise, return False

        ====

        used in combination with the extraction function when acquiring historical data

        if duplicate data is found, halt historical data gathering on current thread and return
    '''
    pass

def data_exists_in_table(transaction_to_check, table_name):
    '''
        check if the given transaction data already exists in the table

        if it does, return True, otherwise, return False
    '''

    if len(transaction_to_check) == 0:
        return True

    # connect to the database
    connection = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={HOST}')
    cursor = connection.cursor()

    # transaction_to_check = TEST_DATA
    # transaction_to_check = [
    #     {
    #         'reporting_owner_name': 'ALLEN MICHELE',
    #         'issuer_name': 'WYNDHAM HOTELS  RESORTS, INC.',
    #         'ticker_symbol': 'WH',
    #         'acceptance_time': datetime(2024, 6, 3, 16, 58, 46),
    #         'security_title': 'Common Stock',
    #         'transaction_date': datetime(2024, 5, 30, 0, 0, tzinfo=timezone(timedelta(days=-1, seconds=61200))),
    #         'deemed_execution_date': None,
    #         'transaction_code': 'S',
    #         'num_transaction_shares': 1274,
    #         'acquired_or_disposed': 'D',
    #         'transaction_share_price': Decimal('67.8100'),
    #         'amount_owned_after_transaction': '25056',
    #         'ownership_form': 'D',
    #         'original_form_4_text_url': 'https://www.sec.gov/Archives/edgar/data/1768145/0001437749-24-019061.txt'
    #     }
    # ]

    built_query = [f'''
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
    original_form_4_text_url
    FROM
    {table_name}
    WHERE '''
    ]

    num_keys = len(transaction_to_check[0].keys())
    filtered_data = []

    for i, (key, value) in enumerate(transaction_to_check[0].items()):
        if value == None and i == num_keys-1:
            built_query.append(f'{key} is NULL')
        elif value != None and i == num_keys-1:
            built_query.append(f'{key}=%s')
            filtered_data.append(value)
        elif value == None:
            built_query.append(f'{key} is NULL AND ')
        elif value != None:
            built_query.append(f'{key}=%s AND ')
            filtered_data.append(value)
    
    finished_query = ''.join(built_query)

    # print(finished_query)
    # print(filtered_data)

    cursor.execute(finished_query, tuple(filtered_data))

    result = cursor.fetchone()
    print(result)

    if result:
        return True
    return False


    

def remove_test_data_row():
    '''
        looks for the TEST_DATA row values and removes the row with that data
    '''
    pass

def check_if_row_exists():
    pass

def view_duplicate_transactions():
    '''
        if there are any duplicates in the transaction table, print them out to see
    '''

    # connect to the database
    connection = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={HOST}')
    cursor = connection.cursor()

    # get all rows of the db
    try:
        cursor.execute(FORM_4_ALL_ROWS_STATEMENT)
        all_rows = cursor.fetchall()
    except psycopg2.Error as postgres_error:
        print(f'Error in selecting all rows from form 4 table: {postgres_error}')


    # iterate through the rows and create a counter data structure for counting
    no_form_4_id_rows = []
    for row in all_rows:
        # if i == 10:
        #     break
        no_form_4_id_rows.append(row[1:])

    form_4_table_counter = Counter(no_form_4_id_rows)

    for element, count in form_4_table_counter.items():
        if count >= 2:
            print(f'{element}: {count}')

    connection.close()
    cursor.close()


def remove_data_older_than_one_year():
    '''
        remove any data older than a year from the transaction table

        use acceptance time to determine which rows to remove
    '''
    connection = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={HOST}')
    cursor = connection.cursor()

    # get the rows that are to be deleted
    try:
        cursor.execute(FORM_4_ALL_ROWS_STATEMENT)
        all_rows = cursor.fetchall()
    except psycopg2.Error as postgres_error:
        print(f'Error in selecting all rows from form 4 table: {postgres_error}')
    
    older_than_year_data = []
    for row in all_rows:
        # 5th column has acceptance time value
        acceptance_time_timestamp = row[4]
        one_year_ago = datetime.now() - timedelta(days=365)

        if acceptance_time_timestamp < one_year_ago:
            older_than_year_data.append(row[1:])
    
    

    # print(len(older_than_year_data))

    columns = [
        'reporting_owner_name',
        'issuer_name',
        'ticker_symbol',
        'acceptance_time',
        'security_title',
        'transaction_date',
        'deemed_execution_date',
        'transaction_code',
        'num_transaction_shares',
        'acquired_or_disposed',
        'transaction_share_price',
        'amount_owned_after_transaction',
        'ownership_form',
        'original_form_4_text_url'
    ]

    for older_row in older_than_year_data:
        # find the same row in the form 4 table and remove it
        built_query = ['SELECT * FROM public.form_4_data WHERE '] # use this to double check rows being deleted
        # built_query = ['DELETE FROM public.form_4_data WHERE '] # delete the rows!
        try:
            filtered_old_row = []
            for i, element in enumerate(older_row):
                if element == None and i != len(older_row) - 1: # not last element in row
                    built_query.append(f'{columns[i]} is NULL AND ')
                elif element == None and i == len(older_row) - 1: # last element in row
                    built_query.append(f'{columns[i]} is NULL')
                elif element != None and i != len(older_row) - 1:
                    built_query.append(f'{columns[i]}=%s AND ')
                    filtered_old_row.append(element)
                elif element != None and i == len(older_row) - 1:
                    built_query.append(f'{columns[i]}=%s')
                    filtered_old_row.append(element)
            
            full_built_query = ''.join(built_query)

            cursor.execute(full_built_query, tuple(filtered_old_row))

            # use with the initial select statement built_query to see the rows that will be deleted
            print(cursor.fetchall())

            # commit to the row being deleted from the table
            # use in combination with the initial delete statement built query
            # connection.commit()

        except psycopg2.Error as postgres_error:
            print(f'Error in row removal: {postgres_error}')



if __name__  == '__main__':
    # remove_data_older_than_one_year()
    data_exists_in_table('dummy', 'form_4_data')