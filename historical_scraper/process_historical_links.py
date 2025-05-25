from datetime import timedelta, datetime
# import os
# import sys
# sys.path.append('/opt/airflow/common_functions')
from extract import scrape_for_SEC_form, extract_non_derivative_form_4_info, xml_to_soup, HEADERS
from transform import filter_out_form_4_data
from bs4 import BeautifulSoup
import requests
import logging
from pprint import pformat
from load import upload_form_4_data
from config import *
from historical_data_scraper import *
import concurrent.futures
import multiprocessing
import time


def threaded_function(func, data):
    # get the total number of available processors
    # max num cpus is actually 16 for local development
    # num_cpus = multiprocessing.cpu_count()

    # use at most 10 threads since SEC only allows 10 requests per second as per
    # https://www.sec.gov/about/webmaster-frequently-asked-questions#code-support
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(func, data)

# form_links = file_links_creator()

def get_form_data(link):
    # takes a url link and gets the data for it for the filing form
    all_processed_form_4_data = []

    # print(' in get form data!')

    try:
        form_data = requests.get(link, headers=HEADERS).content
        # ensure very unlikely for program to exceed 10 request per second limit
        time.sleep(1)
    except requests.exceptions.ConnectionError as connection_error:
        logging.info(f'A connection error occured when trying to connect to the resourcce: {connection_error}')
    except requests.exceptions.ConnectTimeout as timeout_connection:
        logging.info(f'A connection timeout error occured: {timeout_connection}')
    except requests.exceptions.HTTPError as http_error:
        logging.info(f'An http error occured: {http_error}')
    except requests.exceptions.InvalidURL as url_error:
        logging.info(f'An invalid url error occured: {url_error}')
    except requests.exceptions.InvalidHeader as http_header_error:
        logging.info(f'An invalid http header error occured: {http_header_error}')
    except Exception as e:
        logging.info(f'An unexpected error occured, please check: {e}')

    # print('end of get form data try block')

    form_4_soup = xml_to_soup(form_data)
    all_processed_form_4_data.extend(extract_non_derivative_form_4_info(form_4_soup, link))

    return all_processed_form_4_data



def main():
    form_links = []

    # with open('historical_data_links_1_year_strict.txt', 'r', encoding='utf-16') as file:
    with open('historical_data_links_1_year_strict.txt', 'r', encoding='utf-16') as file:
        for line in file:
            form_links.append(line.rstrip('\n'))
    
    all_processed_form_data = threaded_function(get_form_data, form_links)

    all_data_to_process_together = []
    for form_data_list in all_processed_form_data:
        if form_data_list:
            all_data_to_process_together.extend(form_data_list)

    # for data in all_data_to_process_together:
    #     print(data)

    # TODO: use line below when ready to insert the data into the db
    upload_form_4_data(DB_USER, DB_NAME, DB_PASSWORD, HOST, all_data_to_process_together)



if __name__ == '__main__':
    main()
