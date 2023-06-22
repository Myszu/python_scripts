import googlemaps
import pandas as pd

def measure():
    """Script measures distance between locations from CSV file by searching via Google Maps API the given keywords. Column A should contain `Source Location` and B `Destination`.
    As a result it will return a new file with additional column with distance in KM by default, but it can be adjusted by changing `units` variable to imperial.
    """
    # Your list of places to measure distance between. Column
    df = pd.read_csv('./input.csv')
    sources = df.iloc[:,0]
    targets = df.iloc[:,1]

    total = len(sources) + 1

    # Set up the Google Maps client
    api_key = 'YOUR_API_KEY'
    client = googlemaps.Client(api_key)

    output = {}
    output[0] = ['SOURCE', 'DESTINATION', 'DISTANCE']

    for i, source in enumerate(sources):
            
        # Define the two places
        place1 = source
        place2 = targets[i]
        
        try:
            # Get the place details for place1
            place1_autocomplete_result = client.places_autocomplete(input_text=place1)
            place1_place_id = place1_autocomplete_result[0]['place_id']
            place1_details = client.place(place_id=place1_place_id)

            place1_lat = place1_details['result']['geometry']['location']['lat']
            place1_lng = place1_details['result']['geometry']['location']['lng']

            # Get the place details for place2
            place2_autocomplete_result = client.places_autocomplete(input_text=place2)
            place2_place_id = place2_autocomplete_result[0]['place_id']
            place2_details = client.place(place_id=place2_place_id)

            place2_lat = place2_details['result']['geometry']['location']['lat']
            place2_lng = place2_details['result']['geometry']['location']['lng']

            # Get the distance between the places using the Google Maps Distance Matrix API
            result = client.distance_matrix(
                origins=[{'lat': place1_lat, 'lng': place1_lng}],
                destinations=[{'lat': place2_lat, 'lng': place2_lng}],
                mode='driving',
                units='metric'
            )
            
            distance = result['rows'][0]['elements'][0]['distance']['text']
            
        except:
            # Exception is usually thrown when one of the locations can not be recognized by given keyword
            distance = 0

        output[i+1] = [place1, place2, distance]
        
        # Print the distance between the places
        print(f'{round(((i+1)/total)*100, 2)}% | Distance between {place1} and {place2} is: {distance}')
        
    print('Now saving...')
    for row in output:
        df = pd.DataFrame([output[row]])
        df.to_csv('./output.csv', mode='a', index=False, header=False)
    print('Saved!')


if __name__ == '__main__':
    measure()
