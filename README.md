# Reverse geocoding
## Purpose
Many biologists, like myself, do fieldwork covering large areas, collecting samples in multiple localities. Specimens are usually associated with GPS coordinates, but it might be hard to keep track of the names of localities where they were collected.

To solve this problem, I decided stop worrying about road and town names while in the field, and retrieve this information later from Google based on the GPS coordinates.

This script takes a list of latitudes and longitudes and returns the same list, but adding information about park, road, municipality, state and country associated with each record. 

##Usage

This is a command-line program written in [python](https://www.python.org), so you need to have python installed. Also, you need some non-standard libraries: [pandas](http://pandas.pydata.org) and [googlemaps](https://github.com/googlemaps/google-maps-services-python)

To use the program, download it and navigate to the folder where you downloaded. Once in the folder, type `./rev_geocoding.py -h` to view a list of arguments used by the program.

###Examples:

The following will read input.xls as the input table and get results in portuguese.
`./rev_geocoding.py -i input.xls -l pt-BR -k AIzaSyBRcgh0NBzbtx8567HJcixDILCYc`

The following will read input.csv as the input table and get results in British English, with states abbreviated.
`./rev_geocoding.py -i input.csv -l en-GB -s -k AIzaSyBRcgh0NBzbtx8567HJcixDILCYc`

###Required arguments

-i INPUT

The program takes as input a table with named columns. This table could be either in Excel (.xls or .xlsx) or csv format. The only requirement is that the table has a columns named *lat* and a column named *lon*, with records containing values for latitude and longitude, respectively. 
Latitudes and longitudes should be given in decimal degrees format. Other columns will be ignored. Example:

Field number | collector | lat | lon | notes
--- | --- | --- | --- | ---
COL0234 | Medeiros | 42.378715 | -71.115683 | MCZ
COL0246 | Cunha | -25.588286 | -46.610232 | MZSP


-k KEY
You need a Google Maps API Key, which is a unique identifier that google gives to you allowing the use of their mapping service for free. Check the following link for information on how to get one: <https://developers.google.com/maps/web-services/> 


###Optional arguments

-l LANGUAGE

By default, the program returns results in English. If you want results in another language, you have to provide it with the -l option. Check this website for languages supported by Google: https://developers.google.com/maps/faq#languagesupport

-s SHORT NAMES

If you use the option -s, the program will return abbreviated names for states/provinces. For example, MA instead of Massachusetts, or SP instead of São Paulo.

##Output

If run is successful, the program will copy the input table add columns named 'municipality', 'state', 'country', 'route' and 'park'. If the columns already exist, information will be overwritten.

The output will be written to both an Excel and a csv file, named geocoding_results and saved in the folder in which the program was called.
