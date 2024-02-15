import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    radius = 6371  # Radius of Earth in kilometers. Use 3956 for miles
    distance = radius * c

    return distance * 1000  # Convert to meters

def are_close(lat1, lon1, lat2, lon2, threshold_distance=10):
    """
    Check if two GPS coordinates are closer than a threshold distance (in meters)
    """
    distance = haversine(lat1, lon1, lat2, lon2)
    return distance < threshold_distance

# Example usage
coordinate1 = (40.7128, -74.0060)  # New York City coordinates
coordinate2 = (34.0522, -118.2437)  # Los Angeles coordinates
threshold_distance = 10  # 10 meters

if are_close(*coordinate1, *coordinate2, threshold_distance):
    print("The coordinates are within 10 meters of each other.")
else:
    print("The coordinates are not within 10 meters of each other.")
