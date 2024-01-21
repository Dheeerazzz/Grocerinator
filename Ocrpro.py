from flask import Flask, render_template, request, jsonify
import io
import json
import cv2
import numpy as np
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']
    if file:
        # Read the uploaded image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Your image processing and OCR code
        height, width, _ = img.shape
        roi = img[0: height, 100: width]
        _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])

        # OCR API call
        url_api = "https://api.ocr.space/parse/image"
        file_bytes = io.BytesIO(compressedimage)
        result = requests.post(url_api, files={"images\sample_ocr.jpg": file_bytes})
        result = result.content.decode()
        result = json.loads(result)

        parsed_results = result.get("ParsedResults")
        if parsed_results is not None:
            parsed_result = parsed_results[0]
            text_detected = parsed_result.get("ParsedText")
            return jsonify({'result': text_detected})

    return jsonify({'result': 'Error processing image'})

if __name__ == '__main__':
    app.run(debug=True)