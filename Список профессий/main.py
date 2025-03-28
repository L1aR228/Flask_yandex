from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/list_prof/<id>')
def news(id):
    id = id.capitalize()

    if id.lower() == 'ol':
        return render_template('ol.html')
    else:
        print(id)
        return render_template('ul.html')


if __name__ == '__main__':
    app.run(debug=True)
