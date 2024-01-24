import requests


def get_location(search):
    api_key = 'your google maps api key'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={search}&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.text

        # print(data)

        data2 = response.json()

        # Check if there are any results
        if "results" in data2 and data2["results"]:
            location = data2["results"][0]["geometry"]["location"]

            # Displaying the extracted viewport information
            print("Viewport Information:")
            print("latitude:", location["lat"])
            print("longitude:", location["lng"])

            longitude = location["lng"]
            latitude = location["lat"]

            return longitude, latitude
        else:
            print('No results found for the location:', search)
            return 0, 0

    else:
        print('Error fetching location', response.status_code)
        return 0, 0

# Example usage
# location_result = get_location('Your Location')
# print(location_result)
