# Data_challenge_TSP

Objective:
To build an efficient script that finds the closest airport to a given user based on their geolocation and the geolocation of the airport.

Technical Architecture:  
1) Libraries:
- gzip :  It provides a simple interface to compress and decompress files
- csv : It provides a simple interface to import and export "CSV" formated files
- Pool : It provides a convenient means of parallelizing the execution of a function across multiple input values, distributing the input data across processes
- geopy : It is a geocoding library for python which provides Measuring Distance, GeoLocating , GeoCoding. To install this library click  https://github.com/geopy/geopy .

2) Methodology:
* Extraction:
  - Initially the data is exracted and stored in the memory. The airport location data is stored in hash list and the user coordinates is stored in a normal list.
  
* Geodistance_Calculation:
  - It takes a user coordinates as argument and stored as a geo coordinate with help of geopy.
  - All the geo locations for airport are stored as a geo coordinates through geopy.
  - For a input user location, the geodistance is computed considering all the airports location.
  - Among all the distances between the user and airports, the nearest distance is taken in account.
  - Returns user 'uuid' and its nearest airport 'iata_code'.
  
