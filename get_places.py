# Importing googlePlace api module and csv module
from googleplaces import GooglePlaces, types, lang
import csv

# Api key var, and result var to store results 
YOUR_API_KEY = 'api_key'
result = []

#Function for reading the csv file
def readCSV(fileName):
    
    with open(fileName) as sample_data:
        reader = csv.reader(sample_data, delimiter=',')
        next(reader) # skips the first line
        places = []  # store places from the file in here
    
        for row in reader:
            place = {
                'id': row[0],
                'name': row[1],
                'lat': row[2],
                'long': row[3]
            }
            places.append(place)

    return places   # Return places from the file     

def writeCSV(result, fileName):

    with open(fileName, 'w+', newline='') as final_data:  # Opens a csv file for reading and writing
    
        writer = csv.DictWriter(final_data, result[0].keys())
        writer.writeheader()                              # Writes the header 
    
        for row in result:
            writer.writerow(row)                          # Writes the data row wise

def fetchPlaces(google_places, data):  

    # Sends an api request to nearby_search param with the given params
    query_result = google_places.nearby_search(
        keyword=data['name'],
        radius=1,
        lat_lng={'lat': data['lat'], 'lng': data['long']})

    if(query_result.raw_response['status'] == 'ZERO_RESULTS'):
        print("Error")
        item = {
            'id': data['id'],
            'name': data['name'],
            'lat' : str(data['lat']),
            'long' : str(data['long']),
            'categories' : "NULL",
            'full_address': "NULL",
            'international_phone': "NULL",
            'rating': "NULL",
            'place_id': "NULL",
            'map_location': "NULL",
            'website': "NULL",
        }
    else:    
        # Sorts out the required the data from the api request result
        for place in query_result.places:
            # Returned places from a query are place summaries.
            #print(place.name)
            #print(place.geo_location)
            #print(place.rating)
            #print(place.place_id)
        
            # The following method has to make a further API call.
            place.get_details()
            #print(place.details) # A dict matching the JSON response from Google.
            #print(place.formatted_address)
            #print(place.types)
        
            item = {
                'id': data['id'],
                'name': data['name'],
                'lat' : str(data['lat']),
                'long' : str(data['long']),
                'categories' : place.types,
                'full_address': place.formatted_address,
                'international_phone': str(place.international_phone_number),
                'rating': str(place.rating),
                'place_id': place.place_id,
                'map_location': place.url,
                'website': place.website,
            }

        
    result.append(item) # Saves the results of each api call in the result


def main():

    print("[+] Reading data from the file")
    places_info = readCSV('sample_data.csv') # Stores the places from file to places_info
    #print(places_info)
    print("[+] Fetching results...")
    google_places = GooglePlaces(YOUR_API_KEY) # Init the googleplaces module
    for place in places_info:                  # loops all the places api request
        fetchPlaces(google_places, place)      # call fetchPlaces to obtain the results
    
    #print(result)

    print("[+] Writing Data into file...")
    writeCSV(result, 'final_data.csv')         # Stores the data into csv file
    print("[+] Done")

if __name__ == "__main__":
    main()
