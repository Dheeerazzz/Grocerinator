from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load your machine learning models (replace 'model1.joblib', 'model2.joblib', etc. with your actual model files)
models = {
    'Model 1': joblib.load('I_work_flask_here/models ra ungamma/model1.pkl'),
    'Model 2': joblib.load('I_work_flask_here/models ra ungamma/model2.pkl'),
    'Model 3': joblib.load('I_work_flask_here/models ra ungamma/model3.pkl'),
    'Model 4': joblib.load('I_work_flask_here/models ra ungamma/model4.pkl'),
}

@app.route('/')
def index():
    return render_template('index.html', models=models.keys())

@app.route('/predict', methods=['POST'])
def predict():
    selected_model = request.form['model']
    user_input = {key: float(request.form[key]) for key in ['Energy', 'Fat', 'Saturated Fat', 'Carbohydrates', 'Sugars', 'Fiber', 'Proteins', 'Salt']}
    
    model = models[selected_model]
    prediction = model.predict([list(user_input.values())])[0]

    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)