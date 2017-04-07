# Parking Space Finder APIs

## Setup Environment
* Install pip
    * sudo apt-get install python-pip
* Install requirements
    * pip install -r requirements.txt
* Install git
    * sudo apt-get install git    
    
## Setup Application

* Checkout ParkingFinderAPIs from github
    * git clone https://github.com/osg9c1/ParkingFinderAPIs.git
* Run the App    
    * cd ParkingApp/parking_finder_directory
    * python manage.py runserver
    
## Problem Statement:

   Assume that we are building a parking app for SF city and we need two API's.

Build the following REST APIs. (choose Django or Flask)

1. REST API to list all available parking spots. Input params: {lat, lng, radius}
2. REST API to reserve an available parking spot. input params: { parking_spot, time-range }


Optional:
- test cases for the API's
- view existing reservations
- cancel existing reservations
- extend existing reservations.

## Frameworks
DjangoRestFrameWork

##APIs
1. View all available parking spaces
2. View all reserved parking spaces
3. Find parking spaces for a give latitude, longitude, radius
4. Book a parking space
5. Extend a parking space booking
6. Cancel a parking space booking

## Goals for Ver 2.0
Built on the React framework added for a GUI

    
