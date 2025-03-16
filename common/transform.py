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
