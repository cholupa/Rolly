# main loop for the robot
# main boot will start in the idle state
# as the states cycle the button press will start the repeat variable to True and auto cycle when the idle state is hit moving on to the next state until the button is pressed again. There will be timed pauses inbetween states to allow easier use to press the button again if needed to stop the loop

import rolly
from db import database
import numpy
import RPi.GPIO as GPIO
import lgpio
import redis

from time import time,sleep
from datetime import datetime
import math


from client import BotClient
import threading


# Global debugging
DEBUG = True

# set the board 
GPIO.setmode(GPIO.BCM)

#HOST and PORT
HOST = '10.0.0.232'
PORT = 5000


# The currentPath are the steps that the robot takes during a run.
# The first step is always registering the origin and a time stamp.
# Each step will have a time stamp
timeStamp = datetime.now().strftime('%b %d %H:%M:%S')



def main():

    # create the database connection
    dbConn = database.startCon()
    # flushing for testing
    dbConn.flushdb()

    # start the client
    client = BotClient(HOST, PORT)


    # loop controller
    repeat = True

    # get rolly object
    bot = rolly.Rolly()

    # test all devices

    bot.servo.centerServo()
    #currentDistance = bot.echoSensor.pulse()
    #motors move forward, then backward
    stepCount = 1
    pathNum = 1


    while repeat:
        print("Current Step "+str(stepCount))
        if stepCount <= 32:
            try:
                print("Running bot loop")
                bot.run()
                turn, distance = bot.packAction()
                sleep(1)
            except(KeyboardInterrupt,MemoryError):
                repeat = False
                print("Cleaning up")
                sleep(1)
            if turn is not None and distance is not None:
                timeStamp = datetime.now().strftime('%b %d %H:%M:%S')
                currentPath = database.create(dbConn, pathNum, stepCount, distance, turn, timeStamp)
                #forward values to server--> get current record
                latestPath = database.getLatest(dbConn, pathNum)
                # any step in the path will be a distance and a direction = stepVals
                try:
                    print(latestPath['distance'])
                    print(latestPath['turn'])
                    client.send_async(int(float(latestPath['distance'])), int(latestPath['turn']))
                    sleep(1)
                except ConnectionRefusedError:
                    print("Unable to send")

                

        elif stepCount > 32:
            pathNum += 1
            stepCount = 0
        stepCount = stepCount + 1
    GPIO.cleanup()
    print(dbConn.hgetall('P1:S2'))
    dbConn.close()




if __name__ == "__main__":
    main()

