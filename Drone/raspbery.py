from dronekit import connect, VehicleMode
from geopy.geocoders import Nominatim
import json
import requests
import time

def connect_to_vehicle():
    # Connect to the Pixhawk flight controller.
    vehicle = connect('/dev/ttyS0', baud=57600, wait_ready=True)
    return vehicle

def get_current_location():
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode("")
    if location:
        data = {
            'Latitude': location.latitude,
            'Longitude': location.longitude
        }
        return data
    else:
        data = {'message': "Unable to get the location."}
        return data

def move_around(vehicle, direction):
    # Implement your movement logic based on the direction and control the drone.
    if direction.lat_direction == 'north':
        vehicle.simple_goto(vehicle.location.global_frame.lat + 0.0001, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
    elif direction.lat_direction == 'south':
        vehicle.simple_goto(vehicle.location.global_frame.lat - 0.0001, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
    else:
        pass
    
    if direction.lon_direction == 'east':
        vehicle.simple_goto(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon + 0.0001, vehicle.location.global_frame.alt)
    elif direction.lon_direction == 'west':
        vehicle.simple_goto(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon - 0.0001, vehicle.location.global_frame.alt)
    else:
        pass

# Replace 'udp:127.0.0.1:14550' with the actual connection string of your drone.
vehicle = connect_to_vehicle()

url = 'xxx.com/location'
epsilon = 0.0009999
destination_reached = False

while not destination_reached:
    data = get_current_location()
    json_data = json.dumps(data)

    response = requests.post(url, json=json_data)
    
    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        move_around(vehicle, response_data)
        
        # Assuming the server returns a 'distance' key in the response
        if 'distance' in response_data and response_data['distance'] < epsilon:
            destination_reached = True
            print("Destination reached!")
    else:
        print("Error:", response.status_code, response.text)

    time.sleep(1)

# Close the connection to the vehicle when done.
vehicle.close()
