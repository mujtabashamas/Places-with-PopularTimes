# Importing googlePlace api module and csv module
from googleplaces import GooglePlaces, types, lang
import populartimes
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
        print("[-] No data found for ID => " + str(data['id']))
        item = {
            "id": data['id'],
            "name": data['name'],
            "lat": str(data['lat']),
            'long': str(data['long']),
            "place_id": "NULL",
            "address": "NULL",
            "types": "NULL",
            "rating": "NULL",
            "phone_num": "NULL",
            "popularity": "NULL",
            "pt_Monday": "NULL",
            "pt_Tuesday": "NULL",
            "pt_Wednesday": "NULL",
            "pt_Thursday": "NULL",
            "pt_Friday": "NULL",
            "pt_Satday": "NULL",
            "pt_Sunday": "NULL",
            "tw_Monday": "NULL",
            "tw_Tuesday": "NULL",
            "tw_Wednesday": "NULL",
            "tw_Thursday": "NULL",
            "tw_Friday": "NULL",
            "tw_Satday": "NULL",
            "tw_Sunday": "NULL",
            "time_spent": "NULL"
        }
    else:    
        # Sorts out the required the data from the api request result
        popular_times = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL']
        time_waits = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL']
        for place in query_result.places:
            print("[+] Fetching data for ID => " + data['id'] + " & place_id => " + place.place_id)    
            res = populartimes.get_id(YOUR_API_KEY, place.place_id)
            
            if not 'current_popularity' in res:
                res['current_popularity'] = 'NULL'
            if not 'time_spent' in res:
                res['time_spent'] = 'NULL'        
            if not 'populartimes' in res: 
                pass
            else:
                for i in range(len(res['populartimes'])):
                    popular_times[i] = res['populartimes'][i]['data']
            if not 'time_wait' in res: 
                pass
            else:
                for i in range(len(res['time_wait'])):
                    time_waits[i] = res['time_wait'][i]['data']         
            
            item = {
                "id": data['id'],
                "name": data['name'],
                "lat": str(data['lat']),
                'long': str(data['long']),
                "place_id": res['id'],
                "address": res['address'],
                "types": res['types'],
                "rating": str(res['rating']),
                "phone_num": res['international_phone_number'],
                "popularity": str(res['current_popularity']),
                "pt_Monday": popular_times[0],
                "pt_Tuesday": popular_times[1],
                "pt_Wednesday": popular_times[2],
                "pt_Thursday": popular_times[3],
                "pt_Friday": popular_times[4],
                "pt_Satday": popular_times[5],
                "pt_Sunday": popular_times[6],
                "tw_Monday": time_waits[0],
                "tw_Tuesday": time_waits[1],
                "tw_Wednesday": time_waits[2],
                "tw_Thursday": time_waits[3],
                "tw_Friday": time_waits[4],
                "tw_Satday": time_waits[5],
                "tw_Sunday": time_waits[6],
                "time_spent": res['time_spent']
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
