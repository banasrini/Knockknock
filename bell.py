import time
import picamera
import RPi.GPIO as GPIO 
import base64
from Pubnub import Pubnub

#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 0
GPIO.setmode(GPIO.BCM)  # new
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP)  # new
while True:
  #take a reading
  input = GPIO.input(24)
  #if the last reading was low and this one high, print
  if ((not prev_input) and input):
    print("Button pressed")
    with picamera.PiCamera() as camera:
    	camera.start_preview()
    	GPIO.wait_for_edge(17, GPIO.FALLING)  # new
    	camera.capture('/home/pi/Desktop/image.jpg')
    	camera.stop_preview()
  #update previous input
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
  with open("/home/pi/Desktop/image.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    
    #use pubnub to send this over the channel 
    publish_key = 'demo'
	subscribe_key = 'demo'
	channel = 'knock'
	message = str

	pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key)
 
	def callback(message):
    	print('sent the message')

	pubnub.publish(channel, message, callback=callback, error=callback)

  
