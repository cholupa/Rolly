#---MAIN---#
# main loop for the robot
# the main file is responsible for the instantation and loop control of the robot movements
# and the uses the client and database for communication to the server and db

import rolly
from db import database
import RPi.GPIO as GPIO
import redis
from time import sleep
from datetime import datetime
from client import BotClient


#HOST and PORT set
HOST = '10.0.0.232'
PORT = 5000


# The currentPath are the steps that the robot takes during a run.
# The first step is always registering the origin and a time stamp.
# Each step will have a time stamp

def main():

    # create the database connection
    dbConn = database.startCon()
    # start the client
    client = BotClient(HOST, PORT)
    # loop controller
    repeat = True
    # get rolly object
    bot = rolly.Rolly()
    # test all devices
    bot.test()
    stepCount = 1
    pathNum = 1

    # main loop begins with making a turn and distance variable and trying to run the robot loop
    # the cycle should makes sure that the step is complete and ready to send, if not, continue within the robot cycle til the next valie step
    # after the robot finishes a run, then a step should be ready to pack and send to the server
    while repeat:
        print("Current Step "+str(stepCount))
        if stepCount <= 10:
            turn, distance = None, None
            try:
                if bot.stepReady:
                    turn, distance = bot.packAction()
                    print(f"packaction returned - turn{turn}, distance - {distance}")
                    bot.stepReady = False
                    stepCount += 1
                    sleep(0.5)
                else:
                    bot.run()
            except(KeyboardInterrupt,MemoryError):
                repeat = False
                print("Cleaning up")
                GPIO.cleanup()
                sleep(1)
            except Exception as e:
                print(f"Unexpected error: {e}")
            # to make sure an empty step is not recorded, a turn must exist and distance needs a value
            # first make a time stamp, then create an entry for the db
            # then retrieve that entry from the db to send to the server
            if turn is not None and distance is not None:
                timeStamp = datetime.now().strftime('%b %d %H:%M:%S')
                currentPath = database.create(dbConn, pathNum, stepCount, distance, turn, timeStamp)
                #forward values to server--> get current record
                latestPath = database.getLatest(dbConn, pathNum)
                # any step in the path will be a distance and a direction = stepVals
                print(latestPath['distance'])
                print(latestPath['turn'])
                client.send_async(int(float(latestPath['distance'])), int(latestPath['turn']))
                sleep(1)
        # step count defines the path length, if it reaches then reset and exit the loop
        elif stepCount > 10:
            pathNum += 1
            stepCount = 0
            repeat = False

    GPIO.cleanup()
    print(dbConn.hgetall('P1:S2'))
    dbConn.close()




if __name__ == "__main__":
    main()

