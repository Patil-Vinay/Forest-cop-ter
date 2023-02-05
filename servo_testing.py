
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm = GPIO.PWM(18,50)
pwm.start(0)

def Open():
    duty = 2
    while duty <= 10:
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        duty = duty +1
        
def Close():
    pwm.ChangeDutyCycle(2)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

time.sleep(1)
Open()
time.sleep(1)
Close()
pwm.stop()
GPIO.cleanup()
