##### it extracts the last 24 hrs pollutants data from the cpcb ccr website for use

import requests
import json
import pandas as pd
import re
import datetime
import time
import base64
from itertools import product

from typing import Dict, List, Union

from pandas.core.common import flatten


from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



def __init__():
    pass


cookies = {
    '_xsrf': '05c526191be6440093a40b968413ad91',
    'ccr_captcha': '4FEFgAGPGRSnyeyzVcEW1QD2z6UO2RJMJm+9dnsUXHl6RF4GxHVWSdYDPEmr+poy0/vvQ8UL4MA4L/4p3nf0qz0thbFeC/QVxpX6L47HlU5C2zRZ4yJjb+qXI+Zlve4dIBTbCCjp45eUsX5qxEIeGacqUiem/ke2szuRn3r2h1FWWU3PNyzLBZwMQGRgNWQ4YXw/h+Jk4Q/Pwqm2o6zN8SJH3llGBz/Pwn5FxwBMOsheLmFFcMEMaYX6UleSVk/uKVKRpY5h8iuP64dKQzMV5g==',
    'ccr_public': '5HySKRtOu8sp1NjSmEl81CLfppa7Qx7/JHWPRG4xdrBp6Gz59vgf7qLjyqsuwODh5K+4Q4J6xOvI3pMhVd+YEZvUwpUX9q1W0jZa6tMbzS1gLRUEQxRhcsG/K9uao4ecM3nmb/UX0h/ba5feJGbK0+XX7sRemBeDDi956YtEwdcoXxq04/wx9ios6Lbfzw6qQvxhGHBoI8Ki4V5tHyFOrxVyDeTzOw/wWdELO0ZnnxNBBAcQ0qCkmutSG+Pv/lNjNJVJ7k0D8yfiEUSdE725jrITk7zlledI/2wYO2FUhD2RjZI0sptrAcXfI+D1IP/SCKOuUxSZ0AGR5hnfcQaV7IeIqEqd3/yuF/cWCO4twJg='
}


headers = {
    'Accept': 'q=0.8;application/json;q=0.9',
    'Accept-Encoding': 'gzip, deflate, zstd',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Cookie': '_xsrf=f5c704dd251f4a7a979f9cc5cf1f4b94; ccr_captcha="H+liHoaPVPOmj82hgSjgGpQ7OvyV61zH2/4xmyeaRkBI3bX7V3GFdMutUQIPEc8JFZtFdBBLTQHFxpnN4AGkb1lorks4+WrMHu//2ClWYl8rJUvE8mXmy4sOaoCNPqrNjaxUoAeqnvHgx/dZcR8CM42cpdiIN5tCnyZ6i/iZYB0Z13OR7SMMLVULSQYTf5Kp7vmENSxcdl5Eryyrk8Pzmxuo4AFk8IMFunQbW6dlh6j5eOuq7CGUBtIHqKbtOITEDK/UxpByIZUggYNV2VhOsQ=="; ccr_public="JPmvUne2wYfeQY9BN8k739Zsg9T19Af4+24SV+H1jmV8Nh8u0DCxKuUc8yKYXb0q+Zs6bciHcV8SUqjXvkv6uUm+wY64GfDbEwW9tiZ/uDC5Ht5krVbY/F2k+hh4gY7Mh3vrndujNly6+IFq4wrfPXIMmFiQo3P8oO5z/xK2X4nCJYISMwOOzLdNS/fj+djAf66faiSMhK5VpxNgKQuh79f/XrJ60EmVJvHPFLXWaE6zUXX2z+O2pqcfpyXR4ZIQqKAO1py863zfmce9RxBXD4+NdUSyguvSHLCZhjQUVFSC4Y7XbKr0bC1d+1sM3HEKVfyce4UjPN6DaAmuINkvd76XgtKpdOT0VKiPVRpya9w="',
    # 'Cookie': '_xsrf=05c526191be6440093a40b968413ad91; ccr_captcha="4FEFgAGPGRSnyeyzVcEW1QD2z6UO2RJMJm+9dnsUXHl6RF4GxHVWSdYDPEmr+poy0/vvQ8UL4MA4L/4p3nf0qz0thbFeC/QVxpX6L47HlU5C2zRZ4yJjb+qXI+Zlve4dIBTbCCjp45eUsX5qxEIeGacqUiem/ke2szuRn3r2h1FWWU3PNyzLBZwMQGRgNWQ4YXw/h+Jk4Q/Pwqm2o6zN8SJH3llGBz/Pwn5FxwBMOsheLmFFcMEMaYX6UleSVk/uKVKRpY5h8iuP64dKQzMV5g=="; ccr_public="5HySKRtOu8sp1NjSmEl81CLfppa7Qx7/JHWPRG4xdrBp6Gz59vgf7qLjyqsuwODh5K+4Q4J6xOvI3pMhVd+YEZvUwpUX9q1W0jZa6tMbzS1gLRUEQxRhcsG/K9uao4ecM3nmb/UX0h/ba5feJGbK0+XX7sRemBeDDi956YtEwdcoXxq04/wx9ios6Lbfzw6qQvxhGHBoI8Ki4V5tHyFOrxVyDeTzOw/wWdELO0ZnnxNBBAcQ0qCkmutSG+Pv/lNjNJVJ7k0D8yfiEUSdE725jrITk7zlledI/2wYO2FUhD2RjZI0sptrAcXfI+D1IP/SCKOuUxSZ0AGR5hnfcQaV7IeIqEqd3/yuF/cWCO4twJg="',
    'Origin': 'https://airquality.cpcb.gov.in',
    'Referer': 'https://airquality.cpcb.gov.in/ccr/',
}


def __init__():
    pass








##################### main function which will download the data

def get_data(**kwargs) -> Dict[dict, str]:
    payload = _get_payload(**kwargs)
    # print(request_data(payload))
    return request_data(payload)        #dict

######## helper functions
def request_data(payload: str):
    try:
        r = requests.post(
            'https://airquality.cpcb.gov.in/caaqms/comparision_data',
            data=payload, headers=headers, verify=True)
        # print(r.status_code)
        # print(r.text)
        decoded_response = base64.b64decode(r.text)

        if r.status_code == 200 and r.text != "":
            return json.loads(decoded_response.decode("UTF-8"))
        else:
            raise Exception("Payload Error!")
    except Exception as e:
        print(e)


def _construct_payload(**kwargs) -> bytes:
    r = {}
    r["criteria"] = kwargs.get("criteria")
    r["reportFormat"] = "Tabular"
    r["fromDate"] = kwargs.get("from_date")
    r["toDate"] = kwargs.get("to_date")
    r["addedStations"] = [{}]
    r["addedStations"][0]["state"] = kwargs.get("state")
    r["addedStations"][0]["city"] = kwargs.get("city")
    r["addedStations"][0]["parameter"] = kwargs.get("parameter_ids")
    r["addedStations"][0]["parameterName"] = kwargs.get("paramnames")
    r["addedStations"][0]["station"] = kwargs.get("station_id")
    r["addedStations"][0]["stationName"] = kwargs.get("station_name")
    rb = json.dumps(r).encode("utf-8")

    # print('\n\n',rb,'\n')
    return base64.b64encode(rb)


def _get_payload(**kwargs):
    from_date = kwargs.get('from_date')
    to_date = kwargs.get('to_date')
    criteria = kwargs.get('criteria')
    # s_id = kwargs.get('station_id')
    city = kwargs.get('city')
    station_id = kwargs.get('station_id')
    p_id = kwargs.get('p_id')
    state = kwargs.get('state')
    parameters = kwargs.get('parameters')
    station_name = kwargs.get('station_name')
    binary_payload = _construct_payload(state = state, city = city, station_id = station_id, paramnames = parameters, parameter_ids = p_id, criteria = criteria, from_date = from_date, to_date = to_date, station_name = station_name)
    
    # print(binary_payload, '\n')
    return binary_payload




############################################### extracting pollutants data
# downloaded_data = get_data(from_date = '22-4-2024 T16:00:00Z', to_date = '23-4-2024 T15:59:00Z', state = 'Haryana', city = 'Gurugram', criteria = '1 Hours', station_id = 'site_5345', p_id = ['parameter_193', 'parameter_215', 'parameter_194', 'parameter_311', "parameter_312", "parameter_203", "parameter_222"], parameters = ['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'Ozone'], station_name='Sector-51, Gurugram - HSPCB')


def extracting_pollutants_data(from_date, to_date, state, city, criteria, station_id, p_id, parameters, station_name):
    data = get_data(from_date=from_date, to_date=to_date, state=state, city=city, criteria=criteria, station_id=station_id, p_id=p_id, parameters=parameters, station_name=station_name)

    site_info = data['siteInfo']

    parameter_ids = site_info['parameters']
    # print('\n', parameter_ids)

    parameters_list = data['tabularData']['header'][2:]
    # print('\n', parameters_list)

    parameters=[]
    for i in range(len(parameters_list)):
        parameters.append(parameters_list[i]['value'])
    # print('\n',parameters)

    body = data['tabularData']['bodyContent']

    # print(body)

    body_data = {}

    for i in range(len(body)):
        data_entry = []

        from_date = body[i]['from date']
        # data_entry.append(from_date)

        for j in parameter_ids:
            if body[i][j] == None:
                body[i][j] = 0
            data_entry.append(float(body[i][j]))
        
        body_data[from_date] = data_entry
        
    # print('\n',body_data)
    return parameters, body_data
        


## extracting data        
# parameters, pollutants_data = extracting_pollutants_data()
# print(len(pollutants_data))


