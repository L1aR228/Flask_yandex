from flask import Flask, redirect, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def mission():
    param = {}
    param['title'] = 'Домашняя страница'
    return render_template('base.html', **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
