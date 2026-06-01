#--MAIN--#
# The main loop to run the rolly loop
# The main file is in charge of the main loop, managing the client side of the program, and handles the database communication


import rolly
from db import database
import numpy
import RPi.GPIO as GPIO
import lgpio
import redis
from time import time,sleep


import client
import threading


# Global debugging
DEBUG = True

# set the board 
GPIO.setmode(GPIO.BCM)

def main():

    # create the database connection
    database.startCon()

    # loop controller
    repeat = True

    # get rolly object
    bot = rolly.Rolly()

    # test all devices

    bot.servo.centerServo()
    currentDistance = bot.echoSensor.pulse()
    #motors move forward, then backward

    origin = numpy.zeros(2)

    steps = 0
# within the repeat the client connections to the server are constantly being made and closed, the server will constantly accept connections, but the client calling to the server if it is off will throw an error and crash the program. This is why it is put in its own thread, and put into a try block separated from the bot.run() loop.
    while repeat:
        try:
            client.send_async(bot.currentDistance)
        except(ConnectionRefusedError):
            print("Connection disrupted")
        
        try:
            bot.run()
            print(f"Distance:{currentDistance}")
        except(KeyboardInterrupt,MemoryError):
            repeat = False
            print("Cleaning up")
            sleep(1)
            # as an additional safeguard use GPIO to also clean pins in case gpiozero does not catch
            GPIO.cleanup()
    lgpio.gpiochip_close(bot.servo.h)
    GPIO.cleanup()



if __name__ == "__main__":
    main()

