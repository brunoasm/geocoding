#!/usr/bin/env python
### This script uses the Python Client for Google Maps Services to do reverse geocoding
### The input table must have a column named lat and a column named lon
### The output will be the same table as input, but with columns added for municipality, state and country
import googlemaps, sys, pandas
import numpy as np
import argparse

#first, parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help = 'path to input file in csv or xls format', required = True)
parser.add_argument('-k', '--key', help = 'Google Maps Geocoding API key - go to https://developers.google.com/maps/web-services/ to get one', required = True)
parser.add_argument('-k', '--language', help = 'Language in which to display the results. See a list of supported languages in https://developers.google.com/maps/faq#languagesupport', default='en-US')


args = parser.parse_args()

Gkey = args.key
input_table_path = args.input
lang = args.language


# Initiallizing google maps with API key
gmaps = googlemaps.Client(key= Gkey)

# First, read input table for input arguments (excel or csv)

if ".xls" in input_table_path:
    intable = pandas.read_excel(input_table_path)
else:
    intable = pandas.read_csv(input_table_path)

#check if columns for municipality, state and country exist, and add as appropriate
for column in ['municipality', 'state', 'country','route']:
    if column not in intable.columns.values:
        intable[column] = np.nan

#create a smaller dataframe only with variables of interest, to speed up code
latlon = intable[['lat','lon']]
nrow = len(latlon.index)

#iterate over rows, do geocoding and save results to latlon table
for row in latlon.iterrows():
    sys.stdout.write('Reverse geocoding row ' +  str(row[0] + 1) + ' of ' + str(nrow) + '\r')
    sys.stdout.flush()
    revgeocode_result = gmaps.reverse_geocode((row[1]['lat'],row[1]['lon']), language=lang)

    if revgeocode_result: #proceed if found any match
        for i in revgeocode_result[0][u'address_components']: #loop through address components of the first match
            if 'country' in i[u'types']:
                intable.loc[row[0],'country'] = i[u'long_name'] #index rows by number and columns by name
            if 'administrative_area_level_1' in i[u'types']:
                intable.loc[row[0],'state'] = i[u'short_name']
            if 'administrative_area_level_2' in i[u'types']:
                intable.loc[row[0],'municipality'] = i[u'long_name']
            if 'route' in i[u'types']:
                intable.loc[row[0],'route'] = i[u'long_name']

#write results
intable.to_excel('geocoding_results.xls', encoding='utf-8', index = False)
intable.to_csv('geocoding_results.csv', encoding='utf-8', index = False)
print 'Output written to geocoding_results.csv and geocoding_results.xls, with utf-8 encoding'
