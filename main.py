import os
from flask import Flask, request, current_app, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import sys
import os
import cv2

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload_file', methods=['POST'])
def upload_video():
	if 'file' not in request.files:
		print('fail', file=sys.stderr)
		return failure_response('No file')
	file = request.files['file']
	if file.filename == '':
		print('no file', file=sys.stderr)
		return failure_response('No file')
	else:
		filename = secure_filename(file.filename)
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.mov')
		file.save(filepath)
		cap = cv2.VideoCapture(filepath)
		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		return success_response({'filename': filename, 'frames': length})

@app.route('/download/<path:filename>', methods=['GET'])
def download_video(filename):
	uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
	return send_from_directory(uploads, filename)

if __name__ == '__main__':
    app.run()