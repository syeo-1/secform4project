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

HEADERS = {
    'User-agent': 'example@gmail.com',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.sec.gov'
}

# WEBDRIVER = webdriver.Firefox(executable_path = DRIVER_PATH, options = FIREFOX_OPTIONS)

def extract_form_4_text_file_links(file_link):
    '''
        takes a form idx file link, downloads it, extracts all form 4
        file links from it, then subsequently removes the downloaded form idx file
    '''
    all_file_form_4_links = []
    base_url = 'https://www.sec.gov/Archives/'

    response = requests.get(file_link, headers=HEADERS)
    response_status_code = response.status_code


    # print(response_status_code)
    if response_status_code == 200:
        file_content = response.content.split(b'\n')
        for line in file_content:
            split_line = line.split()
            if len(split_line) > 0 and split_line[0] == b'4':
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
    while running_date < todays_date:
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

    while running_date <= end_date and running_date < todays_date:
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

def file_links_creator():
    quarter_file_links = get_quarter_data_links()
    historical_form_4_data_links = generate_form_4_historical_data(quarter_file_links)

    # for file_link in quarter_file_links:
    #     print(file_link)

    for historical_data_link in historical_form_4_data_links:
        print(historical_data_link)
    # return historical_form_4_data_links


if __name__ == '__main__':
    file_links_creator()
    # test = generate_date_ranges_one_year_iso8601()
    # print(test)