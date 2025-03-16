'''
A series of functions to aid in extracting data from form 4 text files
'''

from bs4 import BeautifulSoup

def extract_non_derivative_form_4_info(soup):
    '''
    takes a soup object of xml data and extracts the following fields from form 4

    returns the data below in a python dictionary
    ===
    - amount of shares purchased/sold
    - was this a buy or sell (A/D code)
    - issuer name
    - ticker/trading symbol
    - price at transaction time
    - transaction time
    - data retrieval time
    '''
    num_transaction_shares = soup.select('transactionShares > value')[0].text
    ownership_nature = soup.select('transactionAcquiredDisposedCode > value')[0].text
    issuer_name = soup.select('issuerName')[0].text
    ticker_symbol = soup.select('issuerTradingSymbol')[0].text
    transaction_share_price = soup.select('transactionPricePerShare > value')[0].text
    transaction_time = soup.select('nonDerivativeTransaction > transactionDate > value')[0].text
    acceptance_time = soup.select('acceptance-datetime')[0].text.split()[0]
    # TODO: should have data retrieval time as well
    print(
        num_transaction_shares,
        ownership_nature,
        issuer_name,
        ticker_symbol,
        transaction_share_price,
        transaction_time,
        acceptance_time
    )
    return (
        num_transaction_shares,
        ownership_nature,
        issuer_name,
        ticker_symbol,
        transaction_share_price,
        transaction_time,
        acceptance_time
    )

def xml_to_soup(file):
    '''takes xml formatted text input and returns a Soup xml object'''
    return BeautifulSoup(file, 'lxml')

def main():
    with open(r'C:\Users\seans\OneDrive\Desktop\data-zoomcamp\sec-form4-project\tests\workday_form4.xml') as file:
        # for line in file:
        #     print(line)
        xml_soup = xml_to_soup(file)

    # print(xml_soup.select('nonDerivativeTable'))
    a = xml_soup.find('transactionShares')
    # print(a)
    # print(xml_soup.select('transactionShares > value')[0].text)
    # print(xml_soup.find_all(attrs={'refs': 'value'}))
    extract_non_derivative_form_4_info(xml_soup)

    

if __name__ == '__main__':
    main()
