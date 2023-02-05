from tkinter import *
import tkinter as tk
import RPi.GPIO as GPIO
from DHT11_Python import dht11 
import 
import time
import datetime
import threading
import tkinter.font as tkFont
from PIL import ImageTk,Image

import forestfire_prediction
temperature = forestfire_prediction.temperature
humidity= forestfire_prediction.humidity
prediction = forestfire_prediction.prediction

import serial
import time
import string
import pynmea2
import cv2

import picamera
import picamera.array

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.OUT)
pwm = GPIO.PWM(18,50)
pwm.start(0)

root = tk.Tk()
#image = PhotoImage(file="bg.gif")
#background=Label(root, image=image)
root.geometry("1280x720") #You want the size of the app to be 500x500
root.resizable(0, 0) #Don't allow resizing in the x or y direction

label.grid(row=0, column=0)
cap= cv2.VideoCapture(0)

back = tk.Frame(master=root,bg='black')
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) 
# background.place(x=0,y=0,relwidth=1, relheight=1)

title_Label = Label(root, fg="red", background="#FBB917", text="Forest-Copter", font=("Times New Roman", 50,"bold"))
title_Label.place(x = 300, y=20)


temperature = StringVar()
temperature.set("----"+" °C")

humidity = StringVar()
humidity.set("----"+" %")

prediction= StringVar()
prediction.set("----")

lat = StringVar()
lat.set("----")

lng = StringVar()
lng.set("----")

def Open():
    duty = 2
    while duty <= 10:
        pwm.ChangeDutyCycle(duty)
        time.sleep(0)
        duty = duty +1
        
def Close():
    pwm.ChangeDutyCycle(2)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

temperatureLabel = Label(root, fg="blue", background="#ADFF2F", textvariable=temperature, font=("Arial", 15,"bold"))
temperatureLabel.place(x = 10, y = 680)

humidityLabel = Label(root, fg="blue", background="#ADFF2F", textvariable=humidity, font=("Arial", 15,"bold"))
humidityLabel.place(x = 220, y = 680)

predictionLabel = Label(root, fg="blue", background="#ADFF2F", text="Chance Of Forest Fire: ", font=("Arial", 15,"bold"))
predictionLabel.place(x = 400, y = 680)

predictionLabel = Label(root, fg="blue", background="#ADFF2F", textvariable=prediction, font=("Arial", 15,"bold"))
predictionLabel.place(x = 430, y = 680)

gps_latitude = Label(root, fg="blue", background="#9AFEFF", textvariable=lat , font=("Arial", 15,"bold"))
gps_latitude.place(x = 750, y = 650)

gps_longitude = Label(root, fg="blue", background="#9AFEFF", textvariable=lng, font=("Arial", 15,"bold"))
gps_longitude.place(x = 750, y = 680)

DeliveryLabel = Label(root, fg="white",background ="#000000",text=" Delivery Box: ", font=("Arial", 15,"bold"))
DeliveryLabel.place(x = 10, y = 600)

motorOpenButton = Button(root,fg="black",background="#C0C0C0", text="Open Box", font=("Arial", 15,"bold"), height = 2, width = 10, command=Open)
motorOpenButton.place(x=160 ,y=570)

motorCloseButton = Button(root,fg="black",background="#C0C0C0", text="Close Box", font=("Arial", 15,"bold"), height = 2, width = 10, command=Close)
motorCloseButton.place(x=350 ,y=570)

root.attributes("-fullscreen",True)
root.bind("<e>",exit)

def exit():
    root.quit()

    
def gpssensor():
    root.after(6000, gpssensor)
    while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline()

        if newdata[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(newdata)
            lat=newmsg.latitude
            lng=newmsg.longitude
            gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)

def show_frames():
   root.after(6000, gpssensor)
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   label.after(20, show_frames)

def read_every_second():
    gpssensor()
    win.after(1000, read_every_second)


read_every_second()
show_frames()
root.mainloop()