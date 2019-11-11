import json
from math import cos, asin, sqrt


def load_data(filepath):
    fin = open(filepath, 'r', encoding='utf8')
    data = json.loads(fin.read())
    element_list = data['features']
    fin.close()
    return element_list


def get_biggest_bar(data):
    max_count = 0
    max_element = ''
    for element in data:
        properties = element['properties']
        attributes = properties['Attributes']
        seats_count = attributes['SeatsCount']
        if seats_count > max_count:
            max_count = seats_count
            max_element = element
    return max_element


def get_smallest_bar(data):
    min_count = 99999
    min_element = ''
    for element in data:
        properties = element['properties']
        attributes = properties['Attributes']
        seats_count = attributes['SeatsCount']
        if seats_count < min_count:
            min_count = seats_count
            min_element = element
    return min_element


def distance(lat1, lon1, lat2, lon2):
    if (lat1 == lat2) and (lon1 == lon2):
        return 0

    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...


def get_closest_bar(data, longitude, latitude):
    min_dist = 99999
    min_element = ''
    for element in data:
        geometry = element['geometry']
        coordinates = geometry['coordinates']
        dist = distance(latitude, longitude, coordinates[1], coordinates[0])
        if dist < min_dist:
            min_dist = dist
            min_element = element
    return min_element


if __name__ == '__main__':
    bars_data = load_data('bars.json')
    print('min:', get_smallest_bar(bars_data))
    print('max:', get_biggest_bar(bars_data))
    print('closest:', get_closest_bar(bars_data, 37.2082781854611, 55.965296871411425))
