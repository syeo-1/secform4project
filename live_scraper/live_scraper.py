from datetime import timedelta, datetime
# import os
# import sys
# sys.path.append('/opt/airflow/common_functions')
from live_extract import scrape_for_SEC_form, extract_non_derivative_form_4_info, xml_to_soup, HEADERS
from live_transform import filter_out_form_4_data
from bs4 import BeautifulSoup
import requests
import logging
from pprint import pformat
from live_load import upload_form_4_data
from config import *
import os


form_links = scrape_for_SEC_form(4, 100)
print(form_links)

all_processed_form_4_data = []
# exit(0)


filename = 'temp_daily_data_links.txt'
seen_links = []
if os.path.exists(filename) and os.path.isfile(filename):
    with open(filename, 'r') as f:
        seen_links = [link.strip() for link in f]

new_links = [link for link in form_links if link not in seen_links]
print(new_links)
print('===')
if seen_links:
    # print(seen_links)
    print('seen_links exists!')
    exit(0)


for link in new_links:
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


filter_result = filter_out_form_4_data(all_processed_form_4_data)
filtered_form_data = filter_result[0]
daily_unneeded_links = filter_result[1]
# print(filtered_form_data)
# print(len(filtered_form_data))

upload_form_4_data(DB_USER, DB_NAME, DB_PASSWORD, HOST, filtered_form_data, daily_unneeded_links)