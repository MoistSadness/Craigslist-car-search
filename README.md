The code is a nightmare to read. This is what happens when I dont design the script beforehand lol.

Application searches craigslist for used cars and scrapes the returned html file to search for all the related searches that fit the desired search criteria

Create a bash script that runs the application? Is this even needed?

Import data from the cars.json file
Make the data passed to the function usable
Generates all the required information (like URLs)
Acquires the webpage from craigslist and scrapes all the URLs for the search results from it
    Goes into each of those URLs and scrapes the page for vehicle information (Mileage, price)
Compares the information retrieved to the desired information
    If it is a match, it is added to a list of URLs
    In nto a match, it is ignored
List of URLs with a summary is emailed to the user