import requests
import sys
from map_utils import calculate_spn_for_object, haversine, build_static_map_url

GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x/"
YACA_SEARCH_URL = "https://search-maps.yandex.ru/v1/"
API_KEY_YANDEX = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'  # Ключи берутся из учебника, если вы все же собриайтесь это запускать
API_KEY_SEARCH = '8013b162-6b42-4997-9691-77b7074026e0'  # то советую вставить актуальные ключи


def geocode_address(address):
    params = {
        'apikey': API_KEY_YANDEX,
        'format': 'json',
        'geocode': address
    }
    resp = requests.get(GEOCODE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    coords = None
    try:
        geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        coords_str = geo_object['Point']['pos']
        lon, lat = map(float, coords_str.split())
        coords = (lon, lat)
        address_full = geo_object['metaDataProperty']['GeocoderMetaData']['text']
        return coords, address_full
    except Exception:
        return None, None


def search_nearest_pharmacy(lon, lat):
    # Поиск аптек через API поиска (загрузка из API или по OSM, зависит от вашего сервиса)
    # Для примера — делаем запрос к Яндекс.Картам API или используем Overpass API OSM
    # Здесь — заглушка:
    # Возвращает (долгота, широта, название)
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node
      [amenity=pharmacy]
      (around:2000,{lat},{lon});
    out;
    """
    resp = requests.get(overpass_url, params={'data': query})
    resp.raise_for_status()
    data = resp.json()
    if data['elements']:
        min_dist = float('inf')
        closest = None
        for el in data['elements']:
            dist = haversine((lon, lat), (el['lon'], el['lat']))
            if dist < min_dist:
                min_dist = dist
                closest = el
        name = closest.get('tags', {}).get('name', 'Аптека')
        return closest['lat'], closest['lon'], name, min_dist
    return None, None, None, None


def main():
    address = input("Введите адрес: ")
    coords, full_address = geocode_address(address)
    if not coords:
        print("Не удалось получить координаты по адресу.")
        return

    lon, lat = coords

    width_deg, height_deg = 0.01, 0.01

    spn_x, spn_y = calculate_spn_for_object(width_deg, height_deg)

    lat_b, lon_b, name, dist_m = search_nearest_pharmacy(lon, lat)

    center = [(lon + lon_b) / 2, (lat + lat_b) / 2]
    points = [
        (lon, lat, 'Исходная точка'),
        (lon_b, lat_b, 'Аптека: ' + name)
    ]
    map_url = build_static_map_url(center, (spn_x, spn_y), points)

    resp_map = requests.get(map_url)
    resp_map.raise_for_status()
    with open('map.png', 'wb') as f:
        f.write(resp_map.content)
    print("Карта сохранена как map.png")
    print(f"Расстояние до аптеки: {dist_m / 1000:.2f} км")

    snippet = f"Адрес: {full_address}\n" \
              f"Аптека: {name}\n" \
              f"Расстояние: {dist_m / 1000:.2f} км"
    print(snippet)


if __name__ == "__main__":
    main()
