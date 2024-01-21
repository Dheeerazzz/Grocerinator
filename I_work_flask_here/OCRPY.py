from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_ocr', methods=['POST'])
def process_ocr():
    data = request.get_json()
    base64_image = data['image']

    # Decode base64 image
    image_bytes = base64.b64decode(base64_image)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract
    text_detected = pytesseract.image_to_string(Image.fromarray(gray_img))

    return jsonify({'result': text_detected.strip()})

if __name__ == '__main__':
    app.run(debug=True)
