import requests

OSRM_BASE_URL = "https://router.project-osrm.org"


def get_route(start_lat, start_lon, end_lat, end_lon):
    """
    Fetch shortest route using OSRM
    Returns distance (km), duration (min), and route geometry
    """
    url = f"{OSRM_BASE_URL}/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"

    params = {
        "overview": "full",
        "geometries": "geojson"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if "routes" not in data or len(data["routes"]) == 0:
        raise Exception("No route found")

    route = data["routes"][0]

    return {
        "distance_km": round(route["distance"] / 1000, 2),
        "duration_min": round(route["duration"] / 60, 1),
        "geometry": route["geometry"]["coordinates"]
    }


def is_reachable_within_time(start_lat, start_lon, end_lat, end_lon, max_minutes):
    """
    Check if destination can be reached before food expires
    """
    route = get_route(start_lat, start_lon, end_lat, end_lon)
    return route["duration_min"] <= max_minutes
