__author__ = 'bvenkatesan'

import requests
import json
import prettytable
import csv

areacodes = {}

def load_data(path):
    with open(path, 'r') as data:
        #reader = csv.DictReader(data,' ')
        reader = csv.DictReader(data, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            code = str(row.get('area_code'))
            areacodes[code]= row.get('area_text')


def statisticalAreaName(areaCode):
    #print areacodes
    areaName = areacodes[areaCode]
    #print ' areacode: %s, areaname: %s' %(areaCode, areaName)
    return areaName

def splitseriesid(seriesId):
    #print 'series Id %s' %(seriesId)
    prefix = seriesId[3:5]
    code = seriesId[5:18]
    areaCode = prefix + code
    #print 'from splitseriesid : %s' %(areaCode)
    return areaCode

def processBls(blsareacode):
    load_data('../data/bls.la.area')
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['LAU'+str(blsareacode)+'03'],"startyear":"2010", "endyear":"2014"})
    p = requests.post('http://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    #print json_data
    for series in json_data['Results']['series']:
        period = ''
        year = ''
        value = ''
        x=prettytable.PrettyTable(["series id","year","period","value"])
        seriesId = series['seriesID']
        for item in series['data']:
            annual = item['periodName']
            areaCode = splitseriesid(seriesId)
            areaName = statisticalAreaName(areaCode)
            #process by month

            period = item['period']
            value = item['value']
            year = item['year']
            x.add_row([areaName,year,period,value])
            print '  year: %s, period: %s, value: %s' %(year, period, areaName)

        output = open('../data/'+str(seriesId) + '.txt','w')
        output.write(x.get_string())
        output.close()


if __name__ == '__main__':
    print 'pass an area_code from bls.la.area'
    processBls('ST2600000000000')

    #load_data('/Users/bvenkatesan/Documents/workspace/PyCharmProjects/HelloWorld/bls.la.area')