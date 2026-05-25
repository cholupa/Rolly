# main loop for the robot
# main boot will start in the idle state
# a button press will cycle to the next state for the robot to begin its process
# as the states cycle the button press will start the repeat variable to True and auto cycle when the idle state is hit moving on to the next state until the button is pressed again. There will be timed pauses inbetween states to allow easier use to press the button again if needed to stop the loop

import rolly
from db import database
import numpy
import RPi.GPIO as GPIO
import redis
# set the board 
GPIO.setmode(GPIO.BCM)

# button to start and stop the loop


def main():
    print("Main loop begin.")

    # create the database connection
    database.startCon()

    # loop controller
    repeat = True

    # get rolly object
    bot = rolly.Rolly()

    origin = numpy.zeros(2)

    while repeat:
        try:
            # main loop for bot to perform actions
            # send out a pulse, determine if at an obstruction
            # if at an obstruction determine which direction to turn
            # then move in desired direction

            # after so many steps, return to origin
            repeat = False
        except (KeyboardInterrupt,MemoryError):
            repeat = False
            print("Cleaning up")
            sleep(1)
            # as an additional safeguard use GPIO to also clean pins in case gpiozero does not catch
            GPIO.cleanup()


if __name__ == "__main__":
    main()

