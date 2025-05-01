import requests
from map_utils import calculate_spn


def get_object_size_in_degrees(coords, api_key):
    width_deg = 0.02
    height_deg = 0.01
    return width_deg, height_deg


def find_object_and_add_point(address, api_key, map_center, zoom_level=12):
    geocoder_url = f"https://api.yandex.ru/geocode"
    params = {
        'geocode': address,
        'format': 'json',
        'apikey': api_key
    }
    response = requests.get(geocoder_url, params=params)
    response.raise_for_status()
    data = response.json()

    coords = [37.620070, 55.753630]

    obj_width_deg, obj_height_deg = get_object_size_in_degrees(coords, api_key)

    spn_x, spn_y = calculate_spn(zoom_level, obj_width_deg, obj_height_deg)
    map_params = {
        'll': ','.join(map(str, coords)),
        'spn': f'{spn_x},{spn_y}',
        'l': 'map',
        'pt': f'{coords[0]},{coords[1]},pm2dgl'
    }

    static_map_url = 'https://static-maps.yandex.ru/1.x/'
    map_response = requests.get(static_map_url, params=map_params)
    map_response.raise_for_status()

    with open('map.png', 'wb') as f:
        f.write(map_response.content)

    print(f"Координаты: {coords[0]}, {coords[1]}")


if __name__ == "__main__":
    address = input("Введите адрес объекта: ")
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'  # Ключ возможно не самый актуальный, я его взял с учебника
    find_object_and_add_point(address, api_key, map_center=[37.620070, 55.753630], zoom_level=12)
