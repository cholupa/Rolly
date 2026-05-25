import RPi.GPIO as GPIO

import pwmio

from time import sleep, time

from statemachine import StateMachine, State


import board
import adafruit_ahtx0

from gpiozero import Button, PWMLED

from threading import Thread

from math import floor

print("Imports good")

# set the board mode --> send to main.py
GPIO.setmode(GPIO.BCM)

# MotorDriver class controls the DC motors for wheel movements using PWM
# The motor is controlled physically by using the L293D driver chip and powered by a separate power supply module 9V
class MotorDriver:
    
    # pin numbers for motor 1
    PWMEN1 = 26
    DIRFOR = 13
    DIRREV = 19

    #setup the pins for the motors all outputs , no signal return to GPIO
    #TODO SETUP SECOND MOTOR

    GPIO.setup(PWMEN1, GPIO.OUT)
    GPIO.setup(DIRFOR, GPIO.OUT)
    GPIO.setup(DIRREV, GPIO.OUT)

    def driveFor():
        pass




class ServoDriver:
    pass
class EchoDriver:

    # setup pins
    TRIG = 23
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # pulse the trigger and receive through echo returns the calc distance
    def pulse(self):

        # send the trigger pulse for 10 microseconds
        GPIO.output(self.TRIG, True)
        sleep(0.06)
        GPIO.output(self.TRIG, False)

        #startTime = time()
        #endTime = time()

        while GPIO.input(self.ECHO) == 0:
            startTime = time()

        while GPIO.input(self.ECHO) == 1:
            endTime = time()

        sleep(1)


        elapsedTime = endTime -startTime

        distance = (elapsedTime * 34300) / 2
        print("Outside of loop!")
        print(f"{distance}")

        return distance


# The Rolly class is the controller for all physical components
# controls the statemachine mechanics
class Rolly(StateMachine):

    # States of the machine
    idle = State(initial=True)
    sensing = State()
    moving = State()
    turning = State()

    cycle = (idle.to(sensing)|sensing.to(moving)|moving.to(turning)|turning.to(idle))

    # LED displays for different states

    idleLED = 0
    movingLED = 0
    dbwriteLED = 0

    echoSensor = EchoDriver()



    # transition functions between states

    def on_enter_idle(self):
        pass
    def on_exit_idle(self):
        pass
    def on_enter_sensing(self):
        pass
    def on_exit_sensing(self):
        pass
    def on_enter_moving(self):
        pass
    def on_exit_moving(self):
        pass
    def on_enter_turning(self):
        pass
    def on_exit_turning(self):
        pass



rolly = Rolly()
rolly.echoSensor.pulse()
GPIO.cleanup()






