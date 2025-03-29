from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/distribution')
def index():
    return render_template('ol.html')


if __name__ == '__main__':
    app.run(debug=True)
