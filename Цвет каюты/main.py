from flask import Flask, render_template

app = Flask(__name__)


@app.route('/table/<args>/<args2>')
def index(args, args2):
    argss = args
    argss2 = int(args2)
    color = ''
    age = ''
    # Здесь я специально все так расписал чтобы вам было легче читать
    # По факту все эти условия можно запихнуть в 3-4 строки
    if argss2 < 21 and argss.lower() == 'male':
        color = 'gray'
        age = 'young'
    elif argss2 < 21 and argss.lower() == 'female':
        color = 'pink'
        age = 'young'
    elif argss2 > 21 and argss.lower() == 'male':
        color = 'blue'
        age = 'old'
    elif argss2 > 21 and argss.lower() == 'female':
        color = 'red'
        age = 'old'

    if age == 'old':
        age = 'old.jpeg'
    else:
        age = 'young.webp'
    return render_template('ol.html', color=color, age=age)


if __name__ == '__main__':
    app.run(debug=True)
