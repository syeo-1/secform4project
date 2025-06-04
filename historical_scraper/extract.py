'''
A series of functions to aid in extracting data from form 4 text files
'''

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pytz
import re
from itertools import count
from transform import filter_out_form_4_data
from load import upload_form_4_data
from config import *
import time
from db_management import data_exists_in_table

# refer to fair access section
# https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
# also comment by u/tomtomato0414: https://www.reddit.com/r/webscraping/comments/mpgyil/sec_filings/
HEADERS = {
    'User-agent': 'example2@gmail.com',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.sec.gov'
}

REPORTING_REGEX = re.compile(r".+\(\d+\) \(Reporting\)")
DATETIME_REGEX = re.compile(r"(\d{4}-\d{2}-\d{2})<br/>(\d{2}:\d{2}:\d{2})")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def extract_data_from_SEC_file_url(url_list, extraction_function):
    '''
    takes a list of urls, each of which is a text file representing an SEC filing form
    and applies an extraction function to the text file to retrieve data from it

    returns a list of tuples with the desired data from the file within each tuple
    '''

    result = []

    for url in url_list:
        result.append(extraction_function(url))
    
    return result



def etl_non_derivative_form_4_info(soup, link, return_on_existing_data=True):
    '''
    does the whole etl process for a non derivative price transaction

    takes a soup object of xml data and extracts the following fields from form 4

    returns the data below in a list of python tuples
    ===
    - amount of shares purchased/sold
    - was this a buy or sell (A/D code)
    - issuer name
    - ticker/trading symbol
    - price at transaction time
    - transaction time
    - data retrieval time
    '''

    all_extracted_non_derivative_data = []
    eastern_timezone = pytz.timezone('US/Eastern')


    try:
        reporting_owner_name = soup.select('rptOwnerName')[0].text
        if reporting_owner_name == '':
            reporting_owner_name = None
    except:
        reporting_owner_name = None
    
    try:
        issuer_name = soup.select('issuerName')[0].text
        if issuer_name == '':
            issuer_name = None
    except:
        issuer_name = None

    try:
        ticker_symbol = soup.select('issuerTradingSymbol')[0].text
        if ticker_symbol == '':
            ticker_symbol = None
    except:
        ticker_symbol = None
    
    try:
        acceptance_time_unformatted = soup.select('ACCEPTANCE-DATETIME')[0].text.split()[0]
        datetime_obj = datetime.strptime(acceptance_time_unformatted, '%Y%m%d%H%M%S')
        acceptance_time_formatted = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        # print(f'acceptance time is: {acceptance_time}')
        if acceptance_time_formatted == '':
            acceptance_time_formatted = None
    except:
        acceptance_time_formatted = None
    
    non_derivative_transactions = soup.select('nonDerivativeTransaction')

    for non_derivative_transaction in non_derivative_transactions:

        try:
            security_title = non_derivative_transaction.select('securityTitle > value')[0].text
            if security_title == '':
                security_title = None
        except:
            security_title = None
        
        try:
            transaction_date = non_derivative_transaction.select('transactionDate > value')[0].text
            if transaction_date == '':
                transaction_date = None
        except:
            transaction_date = None

        try:
            deemed_execution_date = non_derivative_transaction.select('deemedExecutionDate')[0].text
            if deemed_execution_date == '':
                deemed_execution_date = None

        except:
            deemed_execution_date = None
        try:
            transaction_code = non_derivative_transaction.select('transactionCoding > transactionCode')[0].text
            if transaction_code == '':
                transaction_code = None
        except:
            transaction_code = None

        try:
            num_transaction_shares = non_derivative_transaction.select('transactionShares > value')[0].text
            if num_transaction_shares == '':
                num_transaction_shares = None
        except:
            num_transaction_shares = None

        try:
            acquired_or_dispose = non_derivative_transaction.select('transactionAcquiredDisposedCode > value')[0].text
            if acquired_or_dispose == '':
                acquired_or_dispose = None
        except:    
            acquired_or_dispose = None

        try:
            transaction_share_price = non_derivative_transaction.select('transactionPricePerShare > value')[0].text
            if transaction_share_price == '':
                transaction_share_price = None
        except:    
            transaction_share_price = None

        try:
            amount_owned_after_transaction = non_derivative_transaction.select('postTransactionAmounts > sharesOwnedFollowingTransaction > value')[0].text
            if amount_owned_after_transaction == '':
                amount_owned_after_transaction = None
        except:    
            amount_owned_after_transaction = None

        try:
            ownership_form = non_derivative_transaction.select('ownershipNature > directOrIndirectOwnership > value')[0].text
            if ownership_form == '':
                ownership_form = None
        except:  
            ownership_form = None
        # extraction_time = datetime.now(eastern_timezone).strftime(DATETIME_FORMAT)

        # print(
        #     reporting_owner_name,
        #     issuer_name,
        #     ticker_symbol,
        #     acceptance_time_formatted,
        #     security_title,
        #     transaction_date,
        #     deemed_execution_date,
        #     transaction_code,
        #     num_transaction_shares,
        #     acquired_or_dispose,
        #     transaction_share_price,
        #     amount_owned_after_transaction,
        #     ownership_form,
        #     link
        #     # extraction_time
        # )
        # print('===')

        data_to_load = [{
            'reporting_owner_name': reporting_owner_name,
            'issuer_name': issuer_name,
            'ticker_symbol': ticker_symbol,
            'acceptance_time': acceptance_time_formatted,
            'security_title': security_title,
            'transaction_date': transaction_date,
            'deemed_execution_date': deemed_execution_date,
            'transaction_code': transaction_code,
            'num_transaction_shares': int(float(num_transaction_shares)),
            'acquired_or_dispose': acquired_or_dispose,
            'transaction_share_price': transaction_share_price,
            'amount_owned_after_transaction': amount_owned_after_transaction,
            'ownership_form': ownership_form,
            'original_form_4_text_url': link
            # extraction_time
        }]

        filtered_data = filter_out_form_4_data(data_to_load)

        if not data_exists_in_table(filtered_data, 'form_4_data'):
            upload_form_4_data(DB_USER, DB_NAME, DB_PASSWORD, HOST, filtered_data)

            print(filtered_data[0])
        elif data_exists_in_table(filtered_data, 'form_4_data') and return_on_existing_data:
            # stop iterating through the data and the threaded function
            return



    # return all_extracted_non_derivative_data

    # a = soup.find_all('nonDerivativeTransaction')
    # print(a)


    # # TODO: should have data retrieval time as well

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

        Example: scrape_for_SEC_form(4, 100)
        
        The above function call retrieves SEC form 4 text file links at 100 elements per page.
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
        
        web_page_info = None

        while web_page_info == None:
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
            
            if not web_page_info:
                print('webpage_info is None. Retrying data retrieval')
                time.sleep(2)

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


def xml_to_soup(file):
    '''takes xml formatted text input and returns a Soup xml object'''
    return BeautifulSoup(file, features='xml')

def is_non_derivative_non_RSU_transaction(form_4_contents):
    '''
    takes form 4 data and returns True if it's both a non-derivative transaction
    and non RSU transaction

    '''

    # if it's not a derivative, the derivative table should be completely empty for its XML
    # looks like if transactionCode value is not one of P, S, G, A, F, I can probably ignore

    # if shares were bought and sold, they must have a shares transacted value and price per share value

    # if it's not RSU based transaction, 
    pass


def main():
    # with open(r'C:\Users\seans\OneDrive\Desktop\data-zoomcamp\sec-form4-project\tests\workday_standard_disposal.xml') as file:
    # with open(r'C:\Users\seans\OneDrive\Desktop\data-zoomcamp\sec-form4-project\tests\jetblue_RSU_acquisition.xml') as file:
    # with open(r'C:\Users\seans\OneDrive\Desktop\data-zoomcamp\sec-form4-project\tests\RSU_with_disposal.xml') as file:
    with open(r'C:\Users\seans\OneDrive\Desktop\data-zoomcamp\sec-form4-project\airflow\dags\tests\softbank_derivative_acquisition.xml') as file:
    # with open(r'C:\Users\seans\OneDrive\Desktop\data-zoomcamp\sec-form4-project\tests\draftking_multi_disposal.xml') as file:
        # for line in file:
        #     print(line)
        xml_soup = xml_to_soup(file)

    # print(xml_soup.select('nonDerivativeTable'))
    a = xml_soup.find('transactionShares')
    # print(a)
    # print(xml_soup.select('transactionShares > value')[0].text)
    # print(xml_soup.find_all(attrs={'refs': 'value'}))
    extract_non_derivative_form_4_info(xml_soup, 'dummy.txt')
    

if __name__ == '__main__':
    # main()

    text_links = scrape_for_SEC_form(4, 100)
    print('==========')
    print(text_links)