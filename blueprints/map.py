import flask
import requests
from flask import render_template, request, session, redirect, flash
import math
from blueprints.cinemas import SPB_CINEMAS

bp = flask.Blueprint("map", __name__, url_prefix="/map")

# Ключ для API геокодирования
GEOCODE_API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'
# Ключ для API статических карт
STATIC_MAPS_API_KEY = '7a4bc255-548a-46bf-a0e0-d3cffbd8bb95'


def get_coordinates(address):
    """Получает координаты по адресу"""
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    geocoder_request = f'{server_address}apikey={GEOCODE_API_KEY}&geocode={address}&format=json'

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        if json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"][
            "found"] == "0":
            return None
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        return float(toponym_coodrinates[0]), float(toponym_coodrinates[1])
    return None


def find_nearest_cinema(user_coords: list[float]):
    """Находит ближайший кинотеатр из статического списка"""
    if not user_coords or len(user_coords) != 2:
        return None

    cinemas_with_distances = []

    for cinema in SPB_CINEMAS:
        # Вычисляем расстояние по формуле гаверсинусов (более точное, чем евклидово)
        lat1, lon1 = math.radians(user_coords[1]), math.radians(user_coords[0])
        lat2, lon2 = math.radians(cinema["coords"][1]), math.radians(cinema["coords"][0])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        distance = 6371 * c * 1000  # Радиус Земли в км, переводим в метры

        cinemas_with_distances.append({
            **cinema,
            "distance": distance
        })

    if not cinemas_with_distances:
        return None

    # Возвращаем ближайший кинотеатр
    return sorted(cinemas_with_distances, key=lambda x: x["distance"])[0]


@bp.route("/", methods=['GET', "POST"])
def show_map():
    if request.method == 'GET':
        session['user_active'] = session.get('user_active', False)
        params = {
            "user_active": session['user_active'],
        }
        return render_template("maps/map.html", **params)

    city = request.form.get("city")
    street = request.form.get("street")
    house = request.form.get("house")
    address = f'{city}, {street}, д{house}'

    user_coords = get_coordinates(address)
    if not user_coords:
        params = {
            "cinema_image": "",
            "cinema_name": None,
            "cinema_address": None
        }
        return render_template("maps/map_image.html", **params)

    cinema = find_nearest_cinema(user_coords)
    if not cinema:
        flash("Не удалось найти кинотеатры поблизости")
        return redirect("/map")

    # Генерируем карту с метками
    map_params = {
        'l': 'map',
        'pt': f"{cinema['coords'][0]},{cinema['coords'][1]}",
        'z': '17',
        'size': '650,450'
    }

    map_url = f"https://static-maps.yandex.ru/1.x/?{'&'.join([f'{k}={v}' for k, v in map_params.items()])}"
    response = requests.get(map_url)

    if response:
        with open('static/movies/images/map.png', "wb") as file:
            file.write(response.content)
        params = {
            "cinema_image": "map.png",
            "cinema_name": cinema["name"],
            "cinema_address": cinema["address"]
        }
        return render_template("maps/map_image.html", **params)

    flash("Ошибка при генерации карты")
    return redirect("/map")
