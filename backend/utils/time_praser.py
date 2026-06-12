def parse_time_to_minutes(time_str: str) -> int:
    """
    Converts time string like:
    - '30 mins'
    - '1 hour'
    - '2.5 hours'
    into total minutes
    """
    time_str = time_str.lower().strip()

    try:
        if "hour" in time_str:
            value = float(time_str.split()[0])
            return int(value * 60)

        if "min" in time_str:
            value = float(time_str.split()[0])
            return int(value)

    except:
        pass

    return 60  # default fallback (1 hour)


def calculate_radius(minutes: int) -> int:
    """
    Dynamic radius logic based on urgency
    """
    if minutes <= 30:
        return 2
    elif minutes <= 60:
        return 4
    elif minutes <= 120:
        return 6
    elif minutes <= 240:
        return 8
    else:
        return 10
