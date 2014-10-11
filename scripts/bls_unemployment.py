__author__ = 'bvenkatesan'

import requests
import json
import prettytable
import csv

state_codes = {}
state_code_file = '../data/bls.state.code'
table=prettytable.PrettyTable(["state code","state name", "year","period","period name", "value"])

def load_state_codes():
    with open(state_code_file, 'r') as data:
        #reader = csv.DictReader(data,' ')
        reader = csv.DictReader(data, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            state_codes[str(row.get('state_code'))] = str(row.get('state_name'))

    print '<---- Loading state codes complete ---->'


def fetchStateData(state_code):
    """
    Series ID    LAUCN281070000000003
	Positions   Value          Field Name
	1-2         LA             Prefix
	3           U              Seasonal Adjustment Code
	4-5         CN             Area Type Code
	6-18        2810700000000  Area Code
	19-20       03             Measure Code
    """
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['LAUST'+str(state_code)+'0000000000003'],"startyear":"2010", "endyear":"2014"})
    p = requests.post('http://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    #print json_data
    for series in json_data['Results']['series']:
        period = ''
        year = ''
        value = ''

        seriesId = series['seriesID']
        for item in series['data']:
            period = item['period']
            periodName = item['periodName']
            value = item['value']
            year = item['year']
            table.add_row([state_code, state_codes.get(state_code), year,period, periodName,value])



def fetchData():
    load_state_codes()

    for state_code in state_codes:
        #print state_code
        data = fetchStateData(state_code)

    output = open('../data/state_unemployment_data' + '.txt','w')
    output.write(table.get_string())
    output.close()


if __name__ == '__main__':
    #load state codes
    fetchData()
