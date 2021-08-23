import flask
from flask import render_template, request, send_from_directory
from flask.templating import render_template_string
from werkzeug.utils import secure_filename
from pathlib import Path

app = flask.Flask(__name__)
upload_folder = Path('uploads')
if not upload_folder.exists():
    upload_folder.mkdir()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        name = secure_filename(photo.filename)
        if name != '':
            path = upload_folder / secure_filename(photo.filename)
            photo.save(path)
            return render_template_string('Upload successful!')
    return render_template('file_upload.html')

@app.route('/gallery', methods=['GET'])
def gallery():
    photos = [p.name for p in upload_folder.glob('*')]
    return render_template('file_list.html', photos=photos)

@app.route('/get_file/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(upload_folder, filename)

app.run(port=8080, debug=True)