import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, render_template, jsonify
import os
import time
import random
import serial

app = Flask(__name__)

# Fetch the service account key JSON file contents
cred = credentials.Certificate('database/real-time-data-2cf5e-firebase-adminsdk-tq12o-74bdce3fbe.json')

# Initialize the app with a None auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://real-time-data-2cf5e-default-rtdb.firebaseio.com',
})  

ref = db.reference('User1')

# Function to check for face-detected images in a directory
def check_for_face_images(directory):
    expanded_directory = os.path.expanduser(directory)
    if os.path.exists(expanded_directory):
        files = os.listdir(expanded_directory)
        for file in files:
            if file.startswith("face"):
                return True
    return False

# Route to check for face-detected images
@app.route('/check_for_face_images')
def check_for_face_images_route():
    directory_path = "~/proj/camera"  # Replace with your directory path
    has_face_images = check_for_face_images(directory_path)
    return jsonify({'has_face_images': has_face_images})

# Route to render the HTML page with the real-time plot
@app.route('/temperature')
def index():
    return render_template('temperature.html')

@app.route('/heartrate')
def heart():
    return render_template('heart_rate.html')

@app.route('/skin_resistance')
def skin_in_the_game():
    return render_template('skin_resistance.html')

# Initializing the serial connection
# ser = serial.Serial('/dev/ttyACM0',115200)
# time.sleep(2)
current_time = time.time()

# Route to fetch real-time data and update the plot
@app.route('/real_time')
def real_time_data():
    # Fetch real-time data (replace with your actual data-fetching logic)
    data = ref.get()
    print(data)
    if data:
        first_key = next(iter(data))
        temperature_data = data[first_key]
        heart_rate_data = data[first_key]
        skin_resistance_data = data[first_key]
        temperature = temperature_data.get("temperature")
        heart_rate = heart_rate_data.get("heart_rate")
        skin_resistance = skin_resistance_data.get("skin_resistance")
        if temperature is None:  # Check if temperature is not found
            return jsonify({'error': 'Temperature data not found'}), 404
        real_time_data = {
            'time': current_time,
            'temperature': temperature,
            'heart_rate': heart_rate,
            'skin_resistance': skin_resistance
        }
        return jsonify(real_time_data)
    """
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            heart_rate, skin_resistance, temperature = map(float, line.split(','))
            real_time_data = {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'heart_rate': heart_rate,
                'skin_resistance': skin_resistance,
                'temperature': temperature
            }
        return jsonify(real_time_data)
        except ValueError:
            return jsonify({'error': 'Malformed input'}), 400
    else:
        return jsonify({'error': 'No data available'}), 400
    """
"""
    current_time = time.time()
    real_time_data = {
        'time': current_time,
        'temperature': random.uniform(20, 30)
    }
    return jsonify(real_time_data)
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
