import cv2 as cv
import base64
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from api.CatRecognition import CheckImage, AddNewClass, TrainFaceRecognizer
from db.utils import get_profile, create_profile

DATABASE_DIR = 'cats'

app = Flask(__name__, 
	static_url_path='',
	static_folder='website')

CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


def get_api_error_response(message, code):
    return jsonify({'message': message}), code


def readb64(encoded_data):
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   return img


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/cat_recognition_api/v1/actions/get_response', methods=['POST'])
def get_model_response():
	params = request.get_json()
	try:
		image = readb64(params.get('image'))
		label = CheckImage(image)

		if label > -1:
			print('Face detected %s' % str(label))
			response = get_profile(label)

		if label == -1:
			response = "Face detected but no match found"

		if label == -2:
			response = "No face detected"

		return jsonify({'response': response})
	except KeyError as e:
		return get_api_error_response('Malformed request, no "%s" param was found' % str(e), 400)
	except ValueError as e:
		return get_api_error_response('Malformed request: %s' % str(e), 400)


@app.route('/cat_recognition_api/v1/actions/add_new_profile', methods=['POST'])
def add_new_profile():
	params = request.get_json()
	try:
		image = params.get('image')
		classes = [readb64(image)]
		profile = create_profile(**params)
		AddNewClass(classes)
		TrainFaceRecognizer(None)
		return jsonify({'response': profile})
	except KeyError as e:
		return get_api_error_response('Malformed request, no "%s" param was found' % str(e), 400)
	except ValueError as e:
		return get_api_error_response('Malformed request: %s' % str(e), 400)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
