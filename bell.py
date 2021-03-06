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
	channel2 = 'pibellchannel'
	message = str

	pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key)
 
	def callback(message):
    	print('sent the message')

	pubnub.publish(channel, message, callback=callback, error=callback)
	
	#subscribing to the 
	def callback(message, channel):
    	if(message == '1')
    		print("open door")
    		#send a message to GPIO to open the door. If the door was already open, leave it open.
    	if(message == '0')
    		print("close door")
    		#send message to close the door. If the door was already closed, leave it close


	def error(message):
    	print("ERROR : " + str(message))


	def connect(message):
    	print("CONNECTED")


	def reconnect(message):
    	print("RECONNECTED")


	def disconnect(message):
   	 print("DISCONNECTED")


pubnub.subscribe(channel=channel2, callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)

  
