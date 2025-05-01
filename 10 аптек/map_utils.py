import math


def calculate_spn_for_object(width_deg, height_deg, map_zoom=12):
    scale_factors = {
        12: (0.05, 0.05),
        10: (0.1, 0.1),
        14: (0.02, 0.02),
    }
    return scale_factors.get(map_zoom, (0.05, 0.05))


def haversine(coord1, coord2):
    R = 6371e3
    lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
    lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def build_static_map_url(center, span, points):
    base_url = 'https://static-maps.yandex.ru/1.x/'
    ll = f"{center[0]},{center[1]}"
    pt_params = []
    for (lon, lat, color) in points:
        pt_params.append(f"{lon},{lat},pm2dgl,shape=circle&icon-color={color}")
    params = {
        'l': 'map',
        'size': '650,450',
        'll': ll,
        'spn': f'{span[0]},{span[1]}',
        'pt': '~'.join(pt_params)
    }
    return base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
