#!/usr/bin/env python
# coding=utf-8

# ----------------------------------
# - NearestDistance.py  28/01/2017 8h21    -
# ----------------------------------

import gzip
import csv
from collections import defaultdict
import geopy, geopy.distance
from multiprocessing import Pool
import shutil
import os


## Read the airport locations and stored into hash 

file_location = gzip.open("../data/optd-sample-20161201.csv.gz", "rt")
data_location = defaultdict(list)
with file_location as data_file:
    reader = csv.DictReader(data_file) 
    for row in reader:
        data_location[row['iata_code']].append(float(row['latitude']))
        data_location[row['iata_code']].append(float(row['longitude']))
file_location.close()

## Read User coordinates

file_user = gzip.open("../data/sample_data.csv.gz", "rt")
with file_user as f:
    reader = csv.reader(f)
    user_list = list(reader)
file_user.close()

## Function for Geodistance calculations of User coordinates with each airport coordinate and return the nearest location to the user.

def geodistance_calculation(user):
    ## Converting hash to a geo-coordinate list with geopy 
    pts = []
    for p in data_location:
        coor = data_location.get(p)
        pts.append(geopy.Point(coor[0],coor[1]))

    print("\nUser Info : ", user[0], "\tCoordinates : " , user[1], user[2])
    onept = geopy.Point(user[1],user[2])
    
    ## Calculating geodistance between user coordinate and all the airports coordinate   
    try:
        alldist = [ (p,geopy.distance.distance(p, onept).km) for p in pts ]
    except Exception:
        alldist = [ (p,geopy.distance.great_circle(p, onept).km) for p in pts ]

    nearest_point, distance = min(alldist, key=lambda x: (x[1]))[0] , min(alldist, key=lambda x: (x[1]))[1] # minimal distance
    print(" Nearest Distance : ", distance ,"\tCoordinates : ", nearest_point[0],", ",nearest_point[1] )
    
    return (user[0],list(data_location.keys())[list(data_location.values()).index([nearest_point[0],nearest_point[1]])])
    

if __name__ == "__main__":
    user_list = user_list[1::]  # Change size of user list to view the results
    
    ## To make it work in paralellize form we have used pool library, so as it can multiprocess, here it uses 4 processes    
    with Pool(4) as pro:
        result_list = pro.map(geodistance_calculation,  user_list, chunksize=10)
        
        ## Writing the list of uuid and its corresponding nearest iata_code to a csv file
        with open('../output/result_file.csv', 'w') as outcsv:   
            writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n') #configure writer to write standard csv file
            writer.writerow(['User_uuid', 'IATA_code'])
            for value in result_list:
                #Write values to outcsv
                writer.writerow([value[0], value[1]])
        
        ## Compressing output file to gzip format        
        with open('../output/result_file.csv', 'rb') as f_in, gzip.open('../output/result_file.csv.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        
        ## Destroying the output file
        os.remove('../output/result_file.csv')







