from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from math import sqrt

# Connect to the Vehicle (SITL in this case)
connection_string = "udp:127.0.0.1:14550"
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

# Arm and take off to 10 meters
arm_and_takeoff(7)

# Go to each waypoint
for waypoint in waypoints:
    print(f"Going to waypoint: {waypoint}")
    vehicle.simple_goto(waypoint, groundspeed=5) 
    
    # Wait until the vehicle reaches the waypoint
    while True:
        current_location = vehicle.location.global_relative_frame
        
        # Debugging output
        print(f"Current location: {current_location}")
        print(f"Waypoint: {waypoint}")
        
        # Ensure the current location is valid
        if current_location.lat == 0 and current_location.lon == 0:
            print("Invalid current location")
            break
        
        distance_to_waypoint = get_distance_meters(current_location, waypoint)
        print(f"Distance to waypoint: {distance_to_waypoint}")
        
        if distance_to_waypoint < 1: 
            print("Reached waypoint")
            time.sleep(3)  # Stablize
            break
        
        time.sleep(1)

# Land the vehicle after reaching the last waypoint
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting the script
vehicle.close()