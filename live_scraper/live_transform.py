'''
functions for transforming data into more acceptable format to be loaded into database
'''
def form_4_data_transform(data):
    '''takes tuple for form4 data and appropriately transforms data'''
    return (
        int(data[0]),
        str(data[1]),
        str(data[2]),
        str(data[3]),
        float(data[4]),
        str(data[5])
    )

def filter_out_form_4_data(all_form_4_data):
    '''
        takes a list of form 4 data points and filters out elements that will not be saved.
        Returns a new list with the data that passes the filter.

        The goal is to only save standard open market purchases or sales of stock.

        The following types of data will not be saved to the database

        - RSU
        - indirect purchases
        - derivatives
        - gifts

    '''

    filtered_form_4_data = []
    unneeded_form_4_links = set()

    for form_4_data in all_form_4_data:
        transaction_code = form_4_data['transaction_code']
        ownership_form = form_4_data['ownership_form']

        # person's ownership must be direct (ie. buyer/seller is actively attempting to buy/sell stock)
        # the transaction must be a standard Purchase, Sell, or for whatever reason, they report a purchase/sell
        # earlier than they have to (V code)
        # for more info: https://www.sec.gov/edgar/searchedgar/ownershipformcodes.html
        if ownership_form == 'D' and transaction_code in ['P', 'S', 'V']:
            filtered_form_4_data.append(form_4_data)
        else:
            # not looking for the other types of data, save it so on subsequent runs don't need to look at it again
            unneeded_form_4_links.add(form_4_data['original_form_4_text_url'])


    return [filtered_form_4_data, unneeded_form_4_links]


