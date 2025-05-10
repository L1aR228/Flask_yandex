from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        images = [f for f in os.listdir(app.config['UPLOAD_FOLDER'])
                  if f.split('.')[-1].lower() in app.config['ALLOWED_EXTENSIONS']]
    except FileNotFoundError:
        images = []

    if request.method == 'POST':
        file = request.files['file']
        if file and '.' in file.filename and \
                file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    return render_template('mars_gallery.html', images=images)


if __name__ == '__main__':
    app.run(debug=True)
