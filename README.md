# Mapping Companies House: Empirical Evidence for the Continuing Need to ‘Think Small First’ in the UK

## Downloading the data and dependencies
You can find the data [here](http://download.companieshouse.gov.uk/en_output.html). The data we analyzed corresponds with June 2021.  
To install dependencies, run ```pip install -r requirements.txt```
## Creating the UK map
Run ``` python create_uk_map.py ```. It takes data of a [grid of the UK](https://www.eea.europa.eu/data-and-maps/data/eea-reference-grids-2/gis-files/great-britain-shapefile).
## Postcode map
First you need to download the dataset [ukpostcodes.csv](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm). Then run ``` python create_postcode.py ```.




