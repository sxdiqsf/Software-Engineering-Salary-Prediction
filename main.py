import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load the dataset
data = pd.read_csv('software_engineer_salaries_india.csv')

# One-hot encoding the education qualification
encoder = OneHotEncoder()
education_encoded = encoder.fit_transform(data[['education_qualification']])

# Convert the encoded education qualification to a DataFrame
education_encoded_df = pd.DataFrame(education_encoded.toarray(), columns=encoder.get_feature_names_out(['education_qualification']))

# Concatenate the original dataset with the encoded features
data = pd.concat([data, education_encoded_df], axis=1)

# Drop the original education_qualification column
data.drop(['education_qualification'], axis=1, inplace=True)

# Define features and target
X = data.drop(['salary'], axis=1)
y = data['salary']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor model
random_forest_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
random_forest_regressor.fit(X_train, y_train)

# Save the model and encoder
joblib.dump(random_forest_regressor, 'random_forest_regressor.pkl')
joblib.dump(encoder, 'encoder.pkl')


from flask import Flask, request, jsonify, render_template, redirect, url_for
import numpy as np
import joblib
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Load the model and encoder
MODEL_PATH = 'random_forest_regressor.pkl'
ENCODER_PATH = 'encoder.pkl'

# Check if the model and encoder files exist
if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
    raise FileNotFoundError("Model or Encoder file not found. Please ensure the files are available.")

random_forest_regressor = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

@app.route('/')
def login():
    return render_template('login2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def home():
    return render_template('indi.html')

@app.route('/')
def back():
    return render_template('login2.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    # Here you would normally check the username and password against a database
    # For simplicity, we'll just allow any non-empty username and password
    if username and password:
        return redirect(url_for('about'))
    return render_template('login.html', error="Invalid credentials, please try again.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        if 'education_qualification' not in data or 'years_of_experience' not in data:
            return jsonify({'error': 'Invalid input data. Please provide education_qualification and years_of_experience.'}), 400
        
        education_qualification = data['education_qualification']
        years_of_experience = data['years_of_experience']
        
        education_encoded = encoder.transform([[education_qualification]]).toarray()
        
        input_array = np.array([years_of_experience] + education_encoded.tolist()[0]).reshape(1, -1)
        
        prediction = random_forest_regressor.predict(input_array)
        
        return jsonify({'predicted_salary': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.run()
