import json
import sys
import os.path
from math import cos, asin, sqrt

bar_latitude = 0
bar_longitude = 0


def load_data(filepath):
    with open(filepath, 'r', encoding='utf8') as file_handle:
        bars_data = json.loads(file_handle.read())
    return bars_data['features']


def get_sets_count(element):
    properties = element['properties']
    attributes = properties['Attributes']
    seats_count = attributes['SeatsCount']
    return seats_count


def get_biggest_bar(bars_data):
    return max(bars_data, key=get_sets_count)


def get_smallest_bar(bars_data):
    return min(bars_data, key=get_sets_count)


def distance_between_points(lat1, lon1, lat2, lon2):
    if (lat1 == lat2) and (lon1 == lon2):
        return 0

    pi_div_180 = 0.017453292519943295        # Pi/180
    a = 0.5 - cos((lat2 - lat1) * pi_div_180)/2 + cos(lat1 * pi_div_180) * cos(lat2 * pi_div_180) * (1 - cos((lon2 - lon1) * pi_div_180)) / 2
    return 12742 * asin(sqrt(a))    # 2*R*asin...


def get_distance(element):
    geometry = element['geometry']
    coordinates = geometry['coordinates']
    distance = distance_between_points(bar_latitude, bar_longitude, coordinates[1], coordinates[0])
    return distance


def get_closest_bar(bars_data):
    return min(bars_data, key=get_distance)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.exists(filename):
            bars_data = load_data(filename)
            print('min:', get_smallest_bar(bars_data))
            print('max:', get_biggest_bar(bars_data))
            try:
                print("Enter bar's longitude (eg. 37.63): ", end='')
                bar_longitude = float(input())
                # bar_longitude = 37.635709999610896
                print("Enter bar's latitude (eg. 55.80): ", end='')
                bar_latitude = float(input())
                # bar_latitude = 55.805575000158512
            except ValueError:
                print("Entered values aren't correct coordinates")
            else:
                print('closest:', get_closest_bar(bars_data))
        else:
            print("Error: File " + filename + " doesn't exist")
    else:
        print('Error: filename is not specified')
