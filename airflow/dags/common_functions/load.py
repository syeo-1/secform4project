import psycopg2
from datetime import datetime
from pytz import timezone

FORM_4_TABLE_STATEMENT = '''
    CREATE TABLE IF NOT EXISTS
    form_4_data
    (
    form_4_id SERIAL,
    number_of_transaction_shares INTEGER,
    transaction_type TEXT,
    issuer_name TEXT,
    ticker_symbol TEXT,
    transaction_share_price NUMERIC(15,4),
    transaction_time DATE,
    acceptance_time TEXT,
    retrieval_time DATE,
    original_file_url TEXT,
    PRIMARY KEY (original_file_url, acceptance_time)
    );
'''

def upload_form_4_data(db_user, db_name, db_password, data):
    '''take a db connection and upload the form 4 data to the appropriate table'''

    table_name = 'form_4_data'
    columns = f'''
        number_of_transaction_shares,
        transaction_type,
        issuer_name,
        ticker_symbol,
        transaction_share_price,
        transaction_time,
        acceptance_time,
        retrieval_time,
        original_file_url
    '''

    connection = psycopg2.connect(f'dbname={db_name} user={db_user} password={db_password}')
    cursor = connection.cursor()

    tz = timezone('US/Eastern')
    data.append(str(datetime.now(tz)))

    try:
        cursor.execute(FORM_4_TABLE_STATEMENT)
        print('Form 4 table successfully generated')
    except psycopg2.Error as postgres_table_creation_error:
        print(f'Error in generating form 4 table in postgres: {postgres_table_creation_error}')

    print(data)
    print(columns)
    print(table_name)
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
            %s
            )
        ''', tuple(data))
        print(f'query to insert price data is successful')
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

if __name__ == '__main__':
    test_data = ['11084', 'D', 'Workday, Inc.', 'WDAY', '253.63', '2025-03-05', '20250307182858']






