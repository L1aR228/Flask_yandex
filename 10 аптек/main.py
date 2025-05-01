import requests
from map_utils import calculate_spn_for_object, haversine, build_static_map_url

GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x/"
OSM_OVERPASS_API = "http://overpass-api.de/api/interpreter"


def geocode_address(address, api_key='f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'):  # Ключ советую поменять
    params = {
        'apikey': api_key,
        'format': 'json',
        'geocode': address
    }
    resp = requests.get(GEOCODE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    try:
        feature = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        coords_str = feature['Point']['pos']
        lon, lat = map(float, coords_str.split())
        full_address = feature['metaDataProperty']['GeocoderMetaData']['text']
        return (lon, lat), full_address
    except Exception as e:
        return None, None


def find_nearby_pharmacies(lon, lat, count=10):
    query = f"""
    [out:json];
    node
      [amenity=pharmacy]
      (around:3000,{lat},{lon});
    out {count};
    """
    resp = requests.get(OSM_OVERPASS_API, params={'data': query})
    resp.raise_for_status()
    data = resp.json()
    pharmacies = []
    for el in data['elements']:
        p_lon, p_lat = el['lon'], el['lat']
        name = el.get('tags', {}).get('name', 'Аптека')
        is_24h = 'opening_hours' in el.get('tags', {})
        is_open_24h = is_24h and (
                '24/7' in el['tags']['opening_hours'] or 'круглосуточно' in el['tags']['opening_hours'])
        pharmacies.append((p_lon, p_lat, name, is_open_24h))
    return pharmacies[:count]


def main():
    address = input("Введите адрес: ")
    coords, full_address = geocode_address(address)
    if not coords:
        print("Не удалось найти координаты по адресу.")
        return
    lon, lat = coords

    width_deg, height_deg = 0.01, 0.01
    span_x, span_y = calculate_spn_for_object(width_deg, height_deg)

    pharmacies = find_nearby_pharmacies(lon, lat, count=10)

    points = []
    for p_lon, p_lat, name, is_24h in pharmacies:
        if is_24h:
            color = '00FF00'  # зелёный
        elif is_24h is False:
            color = '0000FF'  # синий
        else:
            color = '808080'  # серый
        points.append((p_lon, p_lat, f'#{color}'))

    # Центр карты — среднее из двух
    center = [(lon + points[0][0]) / 2, (lat + points[0][1]) / 2]

    map_url = build_static_map_url(center, (span_x, span_y), points)

    resp_map = requests.get(map_url)
    with open('map.png', 'wb') as f:
        f.write(resp_map.content)
    print("Карта сохранена как map.png.")

    print("Ближайшие аптеки:")
    for p_lon, p_lat, name, is_open_24h in pharmacies:
        dist = haversine((lon, lat), (p_lon, p_lat))
        print(f"Название: {name}, Расстояние: {dist / 1000:.2f} км, Круглосуточно: {is_open_24h}")


if __name__ == "__main__":
    main()
