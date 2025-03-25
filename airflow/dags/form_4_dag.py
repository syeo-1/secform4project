from airflow.decorators import task, dag
from datetime import timedelta, datetime
# import os
# import sys
# sys.path.append('/opt/airflow/common_functions')
from common_functions.extract import extract_non_derivative_form_4_info, xml_to_soup, HEADERS
from common_functions.transform import filter_out_form_4_data
from bs4 import BeautifulSoup
import requests


default_args = {
    'owner': 'syeo-1',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id = 'form_4_dag',
    default_args = default_args,
    start_date = datetime(2024, 3, 23),
    schedule_interval = '@once'
)
def form_4_data_pipeline():

    @task
    def retrieve_form_links():
        '''
            retrieves all the links with form 4 data for the last 2 hours
        '''
        # return a single dummy link for now
        # https://www.sec.gov/Archives/edgar/data/1888289/000182176925000039/0001821769-25-000039-index.htm
        # https://www.sec.gov/Archives/edgar/data/1991805/000095015725000265/0000950157-25-000265-index.htm
        return [
            'https://www.sec.gov/Archives/edgar/data/1991805/000095015725000265/0000950157-25-000265.txt'
            'https://www.sec.gov/Archives/edgar/data/1888289/000182176925000039/0001821769-25-000039.txt'
        ]

        

    @task
    def process_form_links(form_links):
        '''
            processes the form data to be saved to the database
        '''

        all_processed_form_4_data = []

        for link in form_links:
            try:
                form_data = requests.get(link, headers=HEADERS).content
            except requests.exceptions.ConnectionError as connection_error:
                print(f'A connection error occured when trying to connect to the resourcce: {connection_error}')
            except requests.exceptions.ConnectTimeout as timeout_connection:
                print(f'A connection timeout error occured: {timeout_connection}')
            except requests.exceptions.HTTPError as http_error:
                print(f'An http error occured: {http_error}')
            except requests.exceptions.InvalidURL as url_error:
                print(f'An invalid url error occured: {url_error}')
            except requests.exceptions.InvalidHeader as http_header_error:
                print(f'An invalid http header error occured: {http_header_error}')
            except Exception as e:
                print(f'An unexpected error occured, please check: {e}')


            form_4_soup = xml_to_soup(form_data)

            all_processed_form_4_data.extend(extract_non_derivative_form_4_info(form_4_soup))
        
        return all_processed_form_4_data

    
    @task
    def filter_form_data(form_data):
        '''
            filters out data not to be saved to the database 
            
            with the focus on form 4 data, this will be all derivative and RSU data mainly to be filtered out
        '''
        return filter_out_form_4_data(form_data)

        
    
    @task
    def load_data(filtered_form_data):
        '''
            load the filtered data to the database connection
        '''
        print(filtered_form_4_data)

    
    form_4_links = retrieve_form_links()
    form_4_data = process_form_links(form_4_links)
    filtered_form_4_data = filter_form_data(form_4_data)
    load_data(filtered_form_4_data)


form_4_dag = form_4_data_pipeline()

