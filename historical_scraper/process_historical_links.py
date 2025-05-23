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


# form_links = file_links_creator()
form_links = []

with open('historical_data_links_1_year.txt', 'r', encoding='utf-16') as file:
    # count = 0
    for line in file:
        # print(line.rstrip('\n'))
        form_links.append(line.rstrip('\n'))
        # print(line.encode('utf-8'))
        # form_links.append(line)
        # print(line)
# print(form_links)
# exit(0)

all_processed_form_4_data = []

for link in form_links:
    try:
        form_data = requests.get(link, headers=HEADERS).content
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

    form_4_soup = xml_to_soup(form_data)

    all_processed_form_4_data.extend(extract_non_derivative_form_4_info(form_4_soup, link))


filtered_form_data = filter_out_form_4_data(all_processed_form_4_data)
# print(filtered_form_data)

upload_form_4_data(DB_USER, DB_NAME, DB_PASSWORD, HOST, filtered_form_data)