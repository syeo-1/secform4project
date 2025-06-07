'''
each day, keep track of the links being used for data extraction

only process new links and whenever a new link comes, place it in the file

use this file to clean up that temporary file at the end of the day. Safe to do at 3am EST the day after
'''
import os

filename = 'temp_daily_data_links.txt'
if os.path.exists(filename) and os.path.isfile(filename):
    os.remove(filename)