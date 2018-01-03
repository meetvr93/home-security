import RPi.GPIO as GPIO
import time
import sys
import requests
import subprocess
import smtplib
from email.mime.text import MIMEText

to = 'gmail id' # Email to send to
gmail_user = 'gmail id' # Email to send from (MUST BE GMAIL)
gmail_password = 'gmail password' # 16-digit Google App Password if using 2-Step Verification

smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)

alert_msg = '------------ALERT! Your Door/Window has been Opened.---------------'

msg = MIMEText(alert_msg)

msg['Subject'] = '[ALERT!!] Home Security may be Breached'
msg['From'] = gmail_user
msg['To'] = to

GPIO.setmode(GPIO.BCM)
WINDOW_SENSOR_PIN = 17
DOOR_SENSOR_PIN = 23
GPIO.setup(WINDOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def readingWindowSensor():
    if GPIO.input(WINDOW_SENSOR_PIN):
        print 'Window opened'
        return 1
    else:
        return 0

def readingDoorSensor():
    if GPIO.input(DOOR_SENSOR_PIN):
        print 'Door opened'
        return 1
    else:
        return 0

def runController():
    windowState = readingWindowSensor()
    if windowState == 1:
        setWindowState('open')
    else:
        setWindowState('closed')
    doorState = readingDoorSensor()
    if doorState == 1:
        setDoorState('open')
    else:
        setDoorState('closed')

def setWindowState(val):
    if val=='open':
        smtpserver.sendmail(gmail_user, [to], msg.as_string())
    values = {'name': val}
    r = requests.put('http://127.0.0.1:8000/window/1/', data=values, auth=('pi', 'Stevens569700'))
    
def setDoorState(val):
    if val=='open':
        smtpserver.sendmail(gmail_user, [to], msg.as_string())
    values = {'name': val}
    r = requests.put('http://127.0.0.1:8000/door/1/', data=values, auth=('pi', 'Stevens569700'))



while True:
    try:
        runController()
        time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
