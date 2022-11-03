'''
Search_For_Car() function takes the user input to search craigslist for the desired car 
and parse the retrieved HTML file for a matching search result

A huge help: https://realpython.com/python-send-email/

Apparently gmail's smtp server does not work most of the time 
https://zetcode.com/python/smtplib/
'''

import SearchCraigslist
import SearchFacebook

import json

search_target = {
    "Location": "sfbay",
    "Model": "Land Cruiser",
    "Year": "2007",
    "Mileage": 180000,
    "Price": 12000
}

'''
Imports data from JSON file and uses it to run the desired searches
'''
def main(search_target):
    MATCHED_VEHICLE_LIST = []

    print("********************************************")
    print("Searching for:\t", search_target["Model"], "\t", search_target["Mileage"], "\t",  search_target["Price"])
    print("********************************************")

    MATCHED_VEHICLE_LIST.extend(SearchCraigslist.Search_Craigslist(
        search_target['Location'],
        search_target['Model'],
        search_target['Year'],
        search_target['Mileage'],
        search_target['Price']
        ))

    '''
    # Open the text file containing car data
    with open("cars.json", "r") as carJSON:
        carList = json.loads(carJSON.read())
        print(carList)
        
        # Iterate through the list of cars and run the search for each one
        for car in range(len(carList)):
            print("********************************************")
            print("Searching for:\t", carList[car]["Model"], "\t", carList[car]["Mileage"], "\t",  carList[car]["Price"])
            print("********************************************")

            # Search Craigslist sfby for cars
            Matched_Vehicles = Search_Craigslist("sfbay", carList[car]["Model"], carList[car]["Mileage"], carList[car]["Price"])

            # .extend adds all newly matched vehicles to MATCHED_VEHICLE_LIST
            MATCHED_VEHICLE_LIST.extend(Matched_Vehicles)
    '''

if __name__ == "__main__":
    main(search_target)