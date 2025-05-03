from flask import Flask, request, render_template_string, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload():
    filename = 'placeholder.png'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        display_image = filename
    else:
        display_image = 'placeholder.png'

    if request.method == 'POST':
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            filename_secure = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename_secure)
            file.save(save_path)
            display_image = filename_secure

    html = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Загрузка фотографии экипажа</title>
        <!-- Bootstrap CDN -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            .container {
                padding-top: 50px;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1 class="mb-4 text-center">Загрузка фотографии экипажа</h1>
        <div class="card mx-auto" style="max-width: 500px;">
            <div class="card-body text-center">
                <form method="POST" enctype="multipart/form-data" class="mb-3">
                    <div class="mb-3">
                        <label for="photo" class="form-label">Выберите фотографию</label>
                        <input class="form-control" type="file" id="photo" name="photo" accept="image/*" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Загрузить</button>
                </form>
                <h5 class="mt-4">Текущая фотография:</h5>
                <img src="{{ url_for('static_file', filename=photo) }}" alt="Фото экипажа" class="img-fluid rounded mt-3" style="max-height: 300px;">
            </div>
        </div>
    </div>
    </body>
    </html>
    '''
    return render_template_string(html, photo=display_image)


@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
