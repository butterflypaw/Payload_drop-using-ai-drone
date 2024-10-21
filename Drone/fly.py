from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from math import sqrt
import socket

# Function to connect to human detection server and get detection result
def get_human_detection():
    host = '127.0.0.1'
    port = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = s.recv(1024)
        # Decode data to get the detection result and distance
        result = data.decode('utf-8').split(',')
        human_detected = result[0] == 'True'
        distance = float(result[1]) if len(result) > 1 else None
        print(f"Human detected: {human_detected}, Distance: {distance} mm")
        return human_detected, distance

# Connect to the Vehicle on COM3
connection_string = "COM3"
vehicle = connect(connection_string, baud=57600, wait_ready=False, heartbeat_timeout=60)

# Function to arm the vehicle and take off to a specified altitude
def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    # Wait until the vehicle is armable
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")  # Change to GUIDED mode to allow for commands
    vehicle.armed = True

    # Wait until the vehicle is armed
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    # Wait until the vehicle reaches a safe height
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95: 
            print("Reached target altitude")
            break
        time.sleep(1)

# Function to calculate distance between two points
def get_distance_meters(location1, location2):
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    return sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5 

# Define waypoints
waypoints = [
    LocationGlobalRelative(17.397157, 78.490406, 6),
    LocationGlobalRelative(17.397034, 78.490396, 6),
    LocationGlobalRelative(17.397052, 78.490212, 6)
]

# Arm and take off to 7 meters
arm_and_takeoff(7)

# Go to each waypoint
for waypoint in waypoints:
    print(f"Going to waypoint: {waypoint}")
    vehicle.simple_goto(waypoint, groundspeed=5)

    while True:
        current_location = vehicle.location.global_relative_frame
        print(f"Current location: {current_location}")
        print(f"Waypoint: {waypoint}")

        if current_location.lat == 0 and current_location.lon == 0:
            print("Invalid current location")
            break

        distance_to_waypoint = get_distance_meters(current_location, waypoint)
        print(f"Distance to waypoint: {distance_to_waypoint}")

        if distance_to_waypoint < 1:
            print("Reached waypoint")
            time.sleep(3)

            # Get human detection result and distance from server
            human_detected, distance = get_human_detection()

            # Act based on the detection result
            if human_detected:
                print(f"Human detected at this waypoint! Distance: {distance} mm. Taking action.")

                # Go to a height of 5 meters above the detected human
                target_altitude = 5  # in meters
                print(f"Descending to {target_altitude} meters...")
                
                # Set the vehicle to GUIDED mode to allow altitude changes
                vehicle.mode = VehicleMode("GUIDED")
                
                # Set the target altitude
                vehicle.simple_goto(LocationGlobalRelative(current_location.lat, current_location.lon, target_altitude))

                # Wait until the drone reaches the target altitude
                while True:
                    current_altitude = vehicle.location.global_relative_frame.alt
                    print(f"Current Altitude: {current_altitude}")
                    
                    if current_altitude >= target_altitude * 0.95:  # Check if within 5% of target altitude
                        print("Reached target altitude of 5 meters")
                        break
                    time.sleep(1)

                # Hover for 10 seconds
                print("Hovering for 10 seconds...")
                time.sleep(10)  # Hover for 10 seconds
                
            else:
                print("No human detected at this waypoint.")
            break
        
        time.sleep(1)

# Land the vehicle after reaching the last waypoint
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Wait for the vehicle to land (altitude close to 0)
while True:
    altitude = vehicle.location.global_relative_frame.alt
    print(f"Current Altitude: {altitude}")
    
    # Break the loop once the vehicle has landed
    if altitude <= 0.1:
        print("Vehicle has landed")
        break
    time.sleep(1)

# Close vehicle object before exiting the script
vehicle.close()