import firebase_admin
from firebase_admin import credentials, db
import serial
import time

# Fetch the service account key JSON file contents
cred = credentials.Certificate('real-time-data-2cf5e-firebase-adminsdk-tq12o-74bdce3fbe.json')

# Initialize the app with a None auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://real-time-data-2cf5e-default-rtdb.firebaseio.com',
})

ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(5)

ref = db.reference('User1')

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        heart_rate, skin_resistance, temperature = map(float, line.split(','))
        data = {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "heart_rate": heart_rate,
            "skin_resistance": skin_resistance,
            "temperature": temperature
        }
        ref.push().set(data)
        print(f"Data saved: {data}")
