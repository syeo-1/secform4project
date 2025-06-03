'''
some functions to see if some stuff works when saving and removing data from the transaction database
'''

from config import *
import psycopg2
from collections import Counter
from datetime import datetime, timedelta

TEST_DATA = {
    'reporting_owner_name': 'Sean Yeo',
    'issuer_name': 'AKGOWEIANGAW',
    'ticker_symbol': 'AGWENGAKWGANW',
    'acceptance_time': '2024-11-14 18:43:14',
    'security_title': 'class C Uncommon 4 stock',
    'transaction_date': '2024-11-14 18:43:14',
    'deemed_execution_date': '2024-11-14 18:43:14',
    'transaction_code': 'S',
    'num_transaction_shares': 43,
    'acquired_or_disposed': 'D',
    'transaction_share_price': 87.23,
    'amount_owned_after_transaction': 4000,
    'ownership_form': 'D',
    'original_form_4_text_ur': 'https://google.com',
}

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

def check_if_duplicate_insertion_possible():
    '''
        check if duplicate row insertion is possible. If it is, then remedy it
    '''
    pass

def remove_test_data_row():
    '''
        looks for the TEST_DATA row values and removes the row with that data
    '''

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
        # built_query = ['SELECT * FROM public.form_4_data WHERE '] # use this to double check rows being deleted
        built_query = ['DELETE FROM public.form_4_data WHERE '] # delete the rows!
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
            # print(cursor.fetchall())

            # commit to the row being deleted from the table
            # use in combination with the initial delete statement built query
            connection.commit()

        except psycopg2.Error as postgres_error:
            print(f'Error in row removal: {postgres_error}')



if __name__  == '__main__':
    remove_data_older_than_one_year()