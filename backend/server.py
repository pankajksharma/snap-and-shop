import os
from flask import Flask
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from compare import return_top_results, get_json

UPLOAD_FOLDER = '/var/www/Snap_and_shop/backend/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return "Hello World!"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/image/<img_name>')
def get_image(img_name):
	return send_from_directory("hackthon/images", img_name)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            best_results = return_top_results(file_name)
            return get_json(best_results)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')