from bs4 import BeautifulSoup
import requests
import pytz
from datetime import datetime, timedelta
import re
from itertools import count

# refer to fair access section
# https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
# also comment by u/tomtomato0414: https://www.reddit.com/r/webscraping/comments/mpgyil/sec_filings/
HEADERS = {
    'User-agent': 'example@gmail.com',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.sec.gov'
}

REPORTING_REGEX = re.compile(".+\(\d+\) \(Reporting\)")
DATETIME_REGEX = re.compile("(\d{4}-\d{2}-\d{2})<br/>(\d{2}:\d{2}:\d{2})")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_reporting_tr_indices(table_row_soup_list):
    indices_list = []

    for i, table_row in enumerate(table_row_soup_list):
        if bool(REPORTING_REGEX.search(table_row.text)):
            # print(table_row)
            indices_list.append(i)
        

    # since the tr element with the actual link is the one right after the one with the "(Reporting)" text in it
    report_link_indices = [x+1 for x in indices_list]

    return report_link_indices


def scrape_for_SEC_form(form_type, items_per_page, start_time=None, end_time=60):
    '''
        Goes to the SEC edgar website looking for the given form type. Goes to the start of the most recent hour on the site
        unless otherwise specified.
    '''

    sec_url = None
    rounded_hour_before_start_datetime = None

    all_formatted_text_links = []

    for page_start in count(start=0, step=100):
        if page_start == 0:
            page_start = ''
            sec_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type={form_type}&SIC=&State=&Country=&CIK=&owner=only&accno=&start={page_start}&count={items_per_page}'
            # print(sec_url)
        else:
            sec_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type={form_type}&SIC=&State=&Country=&CIK=&owner=only&accno=&start={page_start}&count={items_per_page}'
            # print(sec_url)
        
        try:
            web_page_info = requests.get(sec_url, headers=HEADERS).content
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

        page_soup = BeautifulSoup(web_page_info, 'html.parser')
        all_table_row_data = page_soup.find_all('tr')
        # get all indices of table rows in which the text "(Reporting) occurs"
        reporting_text_link_indices = get_reporting_tr_indices(all_table_row_data)
        # print(reporting_text_link_indices)
        tr_link_elements = [all_table_row_data[link_index] for link_index in reporting_text_link_indices]
        # print(tr_link_elements[0])
        # print(tr_link_elements[0])
        formatted_text_links = []
        for tr_link_element in tr_link_elements:
            tablerow_link_soup = BeautifulSoup(f'<table>{tr_link_element}</table>', 'html.parser')
            # print(tr_link_element)
            datetime_match = DATETIME_REGEX.search(str(tr_link_element))
            formatted_table_data_datetime_match_string = f'{datetime_match.group(1)} {datetime_match.group(2)}'
            
            if not start_time:
                start_time = formatted_table_data_datetime_match_string
                start_time_date_object = datetime.strptime(start_time, DATETIME_FORMAT)
                hour_before_start_datetime = start_time_date_object - timedelta(hours=2)
                rounded_hour_before_start_datetime = hour_before_start_datetime.replace(minute=0, second=0)
                # TODO: eventually need it to be searching back until a duplicate is detected in the database, so potentially an hour or more back!
            
            formatted_datetime = datetime.strptime(formatted_table_data_datetime_match_string, DATETIME_FORMAT)

            if formatted_datetime < rounded_hour_before_start_datetime:
                # searching beyond a rounded hour back. So, end the search
                all_formatted_text_links.extend(formatted_text_links)
                return all_formatted_text_links

            unformatted_text_link = [link['href'] for link in tablerow_link_soup.find_all('a') if '.txt' in link['href']][0]
            formatted_text_link = 'https://sec.gov' + unformatted_text_link
            formatted_text_links.append(formatted_text_link)


        all_formatted_text_links.extend(formatted_text_links)
    
    return all_formatted_text_links
        




    

if __name__ == '__main__':
    # get data for last hour, or until (getting a connection to the database) existing data in the db is detected
    # exit(0)
    text_links = scrape_for_SEC_form(4, 100)
    print('==========')
    print(text_links)

