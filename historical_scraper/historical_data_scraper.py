'''
this script will take historical data from SEC website. 
This script will try to retrieve data as far back as 5 years.
I won't be using selenium since it disobeys robots.txt laid out by SEC

Instead, I can get daily transaction information detailed each day in the 
'''

'''
task breakdown:
'''
from datetime import datetime, timedelta, date
import requests
import time
import itertools
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
# import os
# import sys
# sys.path.append('/opt/airflow/common_functions')
from extract import scrape_for_SEC_form, etl_non_derivative_form_4_info, xml_to_soup, HEADERS
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

HEADERS = {
    'User-agent': 'example@gmail.com',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.sec.gov'
}

# WEBDRIVER = webdriver.Firefox(executable_path = DRIVER_PATH, options = FIREFOX_OPTIONS)

def threaded_function(func, data):
    # get the total number of available processors
    # max num cpus is actually 16 for local development
    num_cpus = multiprocessing.cpu_count()

    if num_cpus > 10:
        num_cpus = 10

    # use at most 10 threads since SEC only allows 10 requests per second as per
    # https://www.sec.gov/about/webmaster-frequently-asked-questions#code-support
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cpus) as executor:
        return executor.map(func, data)


def get_form_data(link):
    # takes a url link and gets the data for it for the filing form
    all_processed_form_4_data = []

    # print(' in get form data!')

    try:
        form_data = requests.get(link, headers=HEADERS).content
        # ensure very unlikely for program to exceed 10 request per second limit
        time.sleep(2)
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
    etl_non_derivative_form_4_info(form_4_soup, link, return_on_existing_data=False, cutoff_date=datetime.now()-timedelta(days=5))

def extract_form_4_text_file_links(file_link):
    '''
        takes a form idx file link, downloads it, extracts all form 4
        file links from it, then subsequently removes the downloaded form idx file
    '''
    all_file_form_4_links = []
    base_url = 'https://www.sec.gov/Archives/'

    # for the most current date, try to handle an exception for it
    # in case the data for today/most current date is not ready yet
    try:
        response = requests.get(file_link, headers=HEADERS)
        response_status_code = response.status_code
    except Exception as e:
        print(f'an exception occured: {e}')
        return

    # print(response_status_code)
    if response_status_code == 200:
        file_content = response.content.split(b'\n')
        for line in file_content:
            split_line = line.split()
            if len(split_line) > 0 and split_line[0] == b'4': # only get form 4 data
                all_file_form_4_links.append(base_url + split_line[-1].decode('utf-8'))

    return all_file_form_4_links
    # print(all_file_form_4_links)
        

        

def generate_form_4_historical_data(form_links):
    '''
        takes the form links and goes through each one and passes to the extraction function
        for form data
    '''

    historical_form_4_links = []

    for form_link in form_links:
        historical_form_4_links.extend(extract_form_4_text_file_links(form_link))

    return historical_form_4_links

def generate_date_ranges_one_year_iso8601():
    '''
        gives back all the date strings from up to and including 365 days ago

        excludes the current date
    '''

    todays_date = date.today()
    year_ago = todays_date - timedelta(days=365)

    running_date = year_ago

    date_strings = []
    while running_date <= todays_date:
        date_strings.append(running_date.strftime("%Y%m%d"))
        running_date += timedelta(days=1)

    return date_strings


def generate_quarter_date_ranges_iso8601(year, quarter, year_ago):
    '''
        at most, only give dates to 1 year ago (365 days)
    
        given the year and the quarter, generate list of strings
        in iso8601 format all the dates within that quarter

        make sure the current day is not part of the list!
        Since this is historical data, today's data will only be available via the archives
        the next day, so an error will occur if the script tries to retrieve that data
    '''
    todays_date = date.today()
    quarter_date_range_list = []
    quarter_mapping = [
        {'garbage_value':0},
        {
            'start': f'{year}0101',
            'end': f'{year}0331'
        },
        {
            'start': f'{year}0401',
            'end': f'{year}0630'
        },
        {
            'start': f'{year}0701',
            'end': f'{year}0930'
        },
        {
            'start': f'{year}1001',
            'end': f'{year}1231'
        },
    ]

    chosen_quarter_mapping = quarter_mapping[quarter]
    running_date = datetime.strptime(chosen_quarter_mapping['start'], '%Y%m%d').date()
    end_date = datetime.strptime(chosen_quarter_mapping['end'], '%Y%m%d').date()

    while running_date <= end_date and running_date <= todays_date:
        if running_date >= year_ago:
            quarter_date_range_list.append(running_date.strftime('%Y%m%d'))
        running_date += timedelta(days=1)

    return quarter_date_range_list


def get_quarter_data_links():
    '''
        get all links for each quarter starting from 2020
    '''

    quarter_links = []
    current_year = datetime.now().year
    # print(current_year)
    year_ago = date.today() - timedelta(days=365)

    for year in range(current_year-1, current_year+1):
        for quarter_num in range(1,5):
            if year == 2024 and quarter_num == 1:
                continue
            quarter_dates = generate_quarter_date_ranges_iso8601(year, quarter_num, year_ago)
            for quarter_date in quarter_dates:
                url = f'https://www.sec.gov/Archives/edgar/daily-index/{year}/QTR{quarter_num}/form.{quarter_date}.idx'
                quarter_links.append(url)

    return quarter_links

def extract_and_store_new_data():
    quarter_file_links = get_quarter_data_links()

    # ensure links are ordered in most recent first
    historical_form_4_data_links = reversed(generate_form_4_historical_data(quarter_file_links))

    # for link in historical_form_4_data_links:
    #     print(link)
    # exit(0)

    # process all the links
    threaded_function(get_form_data, historical_form_4_data_links)




    # for file_link in quarter_file_links:
    #     print(file_link)

    # for historical_data_link in reversed(historical_form_4_data_links):
    #     # make sure most recent is first
    #     print(historical_data_link)
    # return historical_form_4_data_links


if __name__ == '__main__':
    extract_and_store_new_data()
    # test = generate_date_ranges_one_year_iso8601()
    # print(test)