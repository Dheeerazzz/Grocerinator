from flask import Flask, render_template, request, jsonify
import io
import cv2
import json
import requests
import base64
import numpy as np

app = Flask(__name__)

# Function to perform OCR on the given image
def perform_ocr(image):
    # Your OCR processing code here...
    height, width, _ = image.shape
    roi = image[0: height, 100: width]

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode("images\sample_ocr.jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                           files={"images\sample_ocr.png": file_bytes},
                           data={"apikey": "K83764290988957",
                                 "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")
    if parsed_results is not None:
        parsed_result = parsed_results[0]
        text_detected = parsed_result.get("ParsedText")
        return text_detected
    else:
        return "ParsedResults is None"

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process_ocr', methods=['POST'])
def process_ocr():
    try:
        # Get the base64-encoded image from the request
        image_data = request.json.get('image')
        image_bytes = io.BytesIO(base64.b64decode(image_data))

        # Perform OCR on the image
        img = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), cv2.IMREAD_COLOR)
        ocr_result = perform_ocr(img)

        return jsonify({'result': ocr_result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
