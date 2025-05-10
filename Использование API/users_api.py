from flask import Flask, request, render_template
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
import requests

app = Flask(__name__)
api = Api(app)

users = {
    1: {"id": 1, "name": "Давид Агаджанян", "email": "davidagadzanan228@gmail.com"},
    2: {"id": 2, "name": "Итачи Учиха", "email": "itachiuchiha@gmail.com"}
}


class UserList(Resource):
    def get(self):
        return list(users.values())

    def post(self):
        data = request.get_json()
        user_id = max(users.keys()) + 1 if users else 1
        user = {
            "id": user_id,
            "name": data["name"],
            "email": data["email"],
            "city_from": data.get("city_from", "Не указан")
        }
        users[user_id] = user
        return user, 201


class User(Resource):
    def get(self, user_id):
        if user_id not in users:
            raise NotFound("User not found")
        return users[user_id]

    def put(self, user_id):
        if user_id not in users:
            raise NotFound("User not found")
        data = request.get_json()
        users[user_id].update({
            "name": data["name"],
            "email": data["email"],
            "city_from": data.get("city_from", users[user_id].get("city_from", "Не указан"))
        })
        return users[user_id]

    def delete(self, user_id):
        if user_id not in users:
            raise NotFound("User not found")
        del users[user_id]
        return "", 204


@app.route('/users_show/<int:user_id>')
def show_user_city(user_id):
    if user_id not in users:
        return "Колонист не найден", 404

    user = users[user_id]
    city = user.get("city_from", "Не указан")

    yandex_api_key = "6c41d71b-e017-4a81-91d0-e9468848f1f9"
    geocoder_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={yandex_api_key}&format=json&geocode={city}"

    try:
        response = requests.get(geocoder_url)
        data = response.json()
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = pos.split()
    except Exception as e:
        lon, lat = "37.617644", "55.755819"

    return render_template('user_city.html',
                           user=user,
                           city=city,
                           lat=lat,
                           lon=lon,
                           yandex_api_key=yandex_api_key)


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
