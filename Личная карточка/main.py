from flask import Flask, render_template
import json
import random
import os

app = Flask(__name__)

print("Содержимое static/img:", os.listdir(os.path.join('static', 'img')))


def load_crew_data():
    json_path = os.path.join('templates', 'crew.json')
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Файл {json_path} не найден!")

    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/member')
def show_member():
    crew_data = load_crew_data()
    random_member = random.choice(crew_data['crew'])
    photo_path = os.path.join('static', random_member['photo'])
    if not os.path.exists(photo_path):
        available_photos = os.listdir(os.path.join('static', 'img'))
        raise FileNotFoundError(
            f"Фото {photo_path} не найдено! Доступные фото: {available_photos}"
        )

    return render_template('member.html', member=random_member)


if __name__ == '__main__':
    app.run(debug=True)
