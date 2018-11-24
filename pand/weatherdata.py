import pandas as pd
import numpy as np
import requests

# https://www.usclimatedata.com/climate/united-states/us

'''
Go to the above address and get a download of state data

to run venv : '. venv/bin/activate'
'''


'''
DataFrame

INDEX1, INDEX2 - Avg High - Avg Low - Avg Rain - Days of Rain - Hours of Sunshine
Jan     Florida
Feb
Mar
Apr
May
Jun
Jul
Aug
Sep
Oct
Nov
Dec

        Georgia

'''
def get_state_dict():
    '''
    Iterate through all states with their associated href to get a dictionary
    return --> {'STATE_NAME':'HREF'}

    '''
    r = requests.get('https://www.usclimatedata.com/climate/united-states/us')
    html_source = r.text
    
    state_table_begin_search = 'Select a state by name'
    table_end = '</table>'

    states_dict = {}
    HREF_LIST = []

    find_begin = html_source.index(state_table_begin_search)
    find_end = html_source[find_begin:].index(table_end) + find_begin
    html_source = html_source[find_begin:find_end+1]

    # Get all HREF links
    cur_href = ''
    for i in range(len(html_source)):
        if html_source[i] == 'h':
            if html_source[i:i+6] == 'href="':
                for j in range(i+6, i+500):
                    if html_source[j] != '"':
                        cur_href += html_source[j]
                    else:
                        HREF_LIST.append(cur_href)
                        cur_href = ''
                        break

    # Use HREF links to create state:href dictionary
    for href in HREF_LIST:
        sub_set = href.split('/')
        # the index of 2 is always the state
        states_dict[sub_set[2]] = href
        
    return states_dict


def get_data_from_state_page(state_href):
    base_url = 'https://www.usclimatedata.com'
    url = base_url + state_href
    
    # ('index1', 'index2') : [col1, col2, col3, col4]
    
    start_key = "var the_data = '["
    end_key = "]';"
    
    data_to_get = ['Month', 'Low', 'High', 'Precipitation']

    r = requests.get(url)
    html_source = r.text

    start = html_source.index(start_key)
    html_source = html_source[start + len(start_key):]
    end = html_source.index(end_key)
    html_source = html_source[:end]

    source_dicts = html_source.split('},{')

    for index, elm in enumerate(source_dicts):
        if index == 0:
            source_dicts[index] = elm + '}'

        elif index == len(source_dicts) - 1:
            source_dicts[index] = '{' + elm

        else:
            source_dicts[index] = '{' + elm + '}'

    for index, item in enumerate(source_dicts):
        source_dicts[index] = eval(item)

    print(source_dicts)

get_data_from_state_page('/climate/hawaii/united-states/3181')

