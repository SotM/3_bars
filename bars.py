import json
from math import cos, asin, sqrt


def load_data(filepath):
    file_handle = open(filepath, 'r', encoding='utf8')
    json_data = json.loads(file_handle.read())
    file_handle.close()
    return json_data['features']


def get_biggest_bar(data):
    max_count = 0
    for element in data:
        properties = element['properties']
        attributes = properties['Attributes']
        seats_count = attributes['SeatsCount']
        max_count = max(seats_count, max_count)
    return max_count


def get_smallest_bar(data):
    min_count = 99999
    for element in data:
        properties = element['properties']
        attributes = properties['Attributes']
        seats_count = attributes['SeatsCount']
        min_count = min(seats_count, min_count)
    return min_count


def distance_between_points(lat1, lon1, lat2, lon2):
    if (lat1 == lat2) and (lon1 == lon2):
        return 0

    pi_div_180 = 0.017453292519943295        # Pi/180
    a = 0.5 - cos((lat2 - lat1) * pi_div_180)/2 + cos(lat1 * pi_div_180) * cos(lat2 * pi_div_180) * (1 - cos((lon2 - lon1) * pi_div_180)) / 2
    return 12742 * asin(sqrt(a))    # 2*R*asin...


def get_closest_bar(data, longitude, latitude):
    min_dist = 99999
    for element in data:
        geometry = element['geometry']
        coordinates = geometry['coordinates']
        dist = distance_between_points(latitude, longitude, coordinates[1], coordinates[0])
        min_dist = min(dist, min_dist)
    return min_dist


if __name__ == '__main__':
    bars_data = load_data('bars.json')
    print('min:', get_smallest_bar(bars_data))
    print('max:', get_biggest_bar(bars_data))
    input_value1 = float(input())
    input_value2 = float(input())
    print('closest:', get_closest_bar(bars_data, input_value1, input_value2))
