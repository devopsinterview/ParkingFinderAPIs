from math import sqrt


def check_parking_in_given_area(center_lat, center_lon, radius, test_lat, test_lon):
    a = center_lat - test_lat
    b = center_lon - test_lon
    dist = sqrt(a*a + b*b)
    if dist < radius:
        return True
    else:
        return False