# Author: Sierra Wells

# Load packages
import sys
import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
from time import time
from random import randint
from warnings import warn
import json
import pandas as pd

# FUNCTIONS
def split_h3(lf):
    assert len(lf) == 1
    lf = str(lf)

    gaza_h3 = "Gaza</h3>"
    wb_h3 = "Occupied West Bank</h3>"
    israel_h3 = "Israel</h3>"

    start_idx_gaza = lf.find(gaza_h3) + len(gaza_h3)
    end_idx_gaza = lf.find(wb_h3)

    start_idx_wb = lf.find(wb_h3) + len(wb_h3)
    end_idx_wb = lf.find(israel_h3)

    start_idx_israel = lf.find(israel_h3) + len(israel_h3)
    end_idx_israel = lf.find("<img", start_idx_israel)
    
    gaza_split = lf[start_idx_gaza:end_idx_gaza]
    wb_split = lf[start_idx_wb:end_idx_wb]
    israel_split = lf[start_idx_israel:end_idx_israel]

    h3_dict = {"gaza": gaza_split,
               "wb": wb_split,
               "israel": israel_split}
    
    return h3_dict

def split_casualty_type(h3_dict):
    for place in h3_dict:
        print(place)
        
 


# Al Jazeera Wayback machine archive URLs
url = 'https://web.archive.org/cdx/search/cdx?url=https://www.aljazeera.com/news/longform/2023/10/9/israel-hamas-war-in-maps-and-charts-live-tracker'

# Parse list of snapshots
snapshots_text = rq.get(url).text

# Separate snapshots by line
snapshots_lines = snapshots_text.strip().split('\n')

# Create a list of lists where each sub-list is split by spaces
sshot_elements = [line.split() for line in snapshots_lines]

# Select only the url for each snapshot
urls = [snapshot[2] for snapshot in sshot_elements]
assert all(url.startswith('http') for url in urls)

# Select only the timestamp for each snapshot
timestamps = [snapshot[1] for snapshot in sshot_elements]
assert all(int(timestamp) > 20231009000000 for timestamp in timestamps)

# Create a data frame with the column urls and timestamps
url_df = pd.DataFrame({'url': urls, 'time': timestamps,
                          'date': [timestamp[:8] for timestamp in timestamps]})

# For each unique date, select the row with the most recent time
url_df = url_df.loc[url_df.groupby('date')['time'].idxmax()]
most_recent_urls = url_df['url'].tolist()

test_url = most_recent_urls[0]
req = rq.get(test_url).text
soup = bs(req,'html.parser')

longform = soup.find_all('div', attrs={"class" : "longform-text"})

lf_split_h3 = split_h3(longform)

split_casualty_type(lf_split_h3)