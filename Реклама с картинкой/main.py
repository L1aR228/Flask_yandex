from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def flask():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def advertisesement():
    sp = ['Человечество вырастает из детства.',
          'Человечеству мала одна планета.', 'Мы сделаем обитаемыми безжизненные пока планеты.',
          'И начнем с Марса!', 'Присоединяйся!']
    return '</br>'.join(sp)


@app.route('/image_mars')
def mars_img():
    return f'''<h1>Жди нас, Марс!</h1> \
           <title>Привет, Марс!</title>\
           <img src="{url_for('static', filename='image.jpeg')}" 
           alt="здесь должна была быть картинка, но не нашлась">
           </br><body>Вот она какая, красная планета.</body>'''


@app.route('/promotion_image')
def img_adv():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='image.jpeg')}" 
           alt="здесь должна была быть картинка, но не нашлась">
                     <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
        
                    <div class="alert alert-primary" role="alert">
                      Человечество вырастает из детства.
                    </div>
                    <div class="alert alert-success" role="alert">
                      Человечеству мала одна планета.
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      Мы сделаем обитаемыми безжизненные пока планеты.
                    </div>
                    <div class="alert alert-warning" role="alert">
                      И начнем с Марса!
                    </div>
                    <div class="alert alert-danger" role="alert">
                      Присоединяйся!
                    </div>
                  </body>
                </html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
