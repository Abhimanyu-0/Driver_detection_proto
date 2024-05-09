import firebase_admin
from firebase_admin import credentials, db
import time
import json
import numpy as np
import scipy

# Fetch the service account key JSON file contents
cred = credentials.Certificate('real-time-data-2cf5e-firebase-adminsdk-tq12o-74bdce3fbe.json')

# Initialize the app with limited server access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://real-time-data-2cf5e-default-rtdb.firebaseio.com',
})

def basic_stats(data):
    print("Mean:", np.mean(data))
    print("Median:", np.median(data))
    print("Mode:", scipy.stats.mode(data)[0])  # Using scipy for mode
    print("Standard Deviation:", np.std(data))
    print("Minimum:", np.min(data))
    print("Maximum:", np.max(data))


# Lists to store data
temperature_l = []
heart_rate_l = []
skin_resistance_l = []

# Reference to the Firebase database path
ref = db.reference('User1')

# Previous key tracker to fetch only new data
last_key = None

while True:
    # Get all entries, starting after the last key processed if available
    data = ref.order_by_key().start_at(last_key).get() if last_key else ref.get()

    if data:
        new_data = False  # Flag to check if new data has been processed
        for key, entry in data.items():
            if last_key and key == last_key:
                continue  # Skip the last processed key if it's included

            new_data = True  # Set flag as new data is being processed
            print(f"Processing entry with key {key}: {entry}")

            # Extract and append data if available and valid
            if isinstance(entry, dict):
                temperature = entry.get('temperature')
                heart_rate = entry.get('heart_rate')
                skin_resistance = entry.get('skin_resistance')

                if temperature is not None:
                    temperature_l.append(temperature)
                if heart_rate is not None:
                    heart_rate_l.append(heart_rate)
                if skin_resistance is not None:
                    skin_resistance_l.append(skin_resistance)

        if new_data:
            last_key = key  # Update the last key only if new data was processed

    # Print sizes of lists to monitor data collection
    print(f"Temperatures: {len(temperature_l)}, Heart Rates: {len(heart_rate_l)}, Skin Resistances: {len(skin_resistance_l)}")
    print("Heart Rate Stats:")
    basic_stats(heart_rate_l)
    print("\nTemperature Stats:")
    basic_stats(temperature_l)
    print("\nSkin Resistance Stats:")
    basic_stats(skin_resistance_l)

    # Sleep for some time before fetching new data again
    time.sleep(10)
