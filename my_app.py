from flask import Flask, request, jsonify, render_template
import base64
import requests
import json
import joblib

app = Flask(__name__)

# OCR API key
OCR_API_KEY = 'K88288596988957'


model_babies = joblib.load('models ra ungamma/model1.pkl')
model_adults = joblib.load('models ra ungamma/model2.pkl')
model_lose_weight = joblib.load('models ra ungamma/model3.pkl')
model_gain_weight = joblib.load('models ra ungamma/model4.pkl')

@app.route('/')
def index():
    # Render the index.html template
    return render_template('main.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    # Receive image data from the frontend
    data = request.json
    image_data_str = data['image']
    
    # Convert the base64-encoded string to bytes
    image_data_bytes = base64.b64decode(image_data_str)

    # Save the received image locally (optional)
    with open('captured_image.png', 'wb') as f:
        f.write(image_data_bytes)

    # Call the OCR API to process the image
    ocr_result = ocr_space_file('captured_image.png', api_key=OCR_API_KEY)

    # Parse the JSON response
    ocr_result_json = json.loads(ocr_result)

    # Extract the useful text from the OCR result
    parsed_text = ocr_result_json['ParsedResults'][0]['ParsedText']

    # Return the useful text
    return jsonify({'result': parsed_text})

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


@app.route('/process_form', methods=['POST'])
def process_form():
    selected_option = request.form['option']
    
    fats = float(request.form['fats'])
    saturated_fats = float(request.form['saturated_fats'])
    carbohydrates = float(request.form['carbohydrates'])
    energy = float(request.form['energy'])
    sugar = float(request.form['sugar'])
    fiber = float(request.form['fiber'])
    protein = float(request.form['protein'])
    salt = float(request.form['salt'])

    if selected_option == 'babies':
        model = model_babies
    elif selected_option == 'adults':
        model = model_adults
    elif selected_option == 'lose_weight':
        model = model_lose_weight
    elif selected_option == 'gain_weight':
        model = model_gain_weight

    input_data = [[fats, saturated_fats, carbohydrates, energy, sugar, fiber, protein, salt]]
    predicted_values = model.predict(input_data)
    return jsonify({'predicted_values': predicted_values.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
