from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance (km) between two GPS points
    """
    R = 6371  # Earth radius in KM

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


def is_within_radius(src_lat, src_lon, dest_lat, dest_lon, radius_km):
    """
    Check if destination is within allowed radius
    """
    distance = haversine(src_lat, src_lon, dest_lat, dest_lon)
    return distance <= radius_km
