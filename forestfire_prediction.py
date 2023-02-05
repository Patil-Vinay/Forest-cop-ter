import RPi.GPIO as GPIO
import dht11
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
import smtplib

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin =4)

#features and labels
features = []
labels = []

while True:
    # get sensor data
    result = instance.read()
    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity
        features.append([temperature, humidity])
        #print("Temperature: %d C" % temperature)
        #print("Humidity: %d %%" % humidity)
    else:
        print("Error: %d" % result.error_code)
        
    # preprocessing
    X, Y = features,labels
    sc_features = StandardScaler()
    X = sc_features.fit_transform(X)
    X = pd.DataFrame(X, columns = features.columns)
    
    # load model
    model = load_model('forest_fire_model.h5')
    
    # make predictions
    predictions = model.predict(X)
    predictions = [1 if x > 0.5 else 0 for x in predictions]
    
    # check for forest fire
    if predictions[-1] == 1:
	prediction = "Yes"
        print("ALERT: Forest fire detected!")
    else:
	prediction = "No"
        print("No forest fire detected.")
