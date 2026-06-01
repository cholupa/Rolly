###----ROLLY----###
# This file is for the actual control of the robot. The classes involved in this files handle all of the physical mechanics
# and main logic causing the robot to move, relay display patterns for the leds, and gathers the sensor data.
# 
# There are 4 classes involved, 3 are components of the robot.
# EchoDriver
# MotorDriver
# ServoDriver
# Rolly
#
# Rolly is a composite of the driver classes to encase the functions of the peripherals into a single class.
#
#
#
#
#
#UPDATES: Button class removed, runs begin from computer through ssh connection, new motor driver chips ordered

#
#####################

import RPi.GPIO as GPIOHave you changed your career plans? If so, what prompted this change? If not, why have you remained with your original plan?
How has your thinking about your career evolved?
Have you completed any research about your choice of career? How has this impacted your thinking? Have you thought about seeking an advanced degree or certification after earning your undergraduate degree?
Which course outcomes have you achieved so far, and which ones remain?

from time import sleep, time

from statemachine import StateMachine, State

import board
import adafruit_ahtx0

from gpiozero import PWMLED, Motor

import lgpio


from math import floor



# Global Debug

DEBUG = True

if DEBUG:
    print("Imports good")


# set the board mode --> send to main.py
GPIO.setmode(GPIO.BCM)

# -MotorDriver class controls the DC motors for wheel movements using Have you changed your career plans? If so, what prompted this change? If not, why have you remained with your original plan?
How has your thinking about your career evolved?
Have you completed any research about your choice of career? How has this impacted your thinking? Have you thought about seeking an advanced degree or certification after earning your undergraduate degree?
Which course outcomes have you achieved so far, and which ones remain?PWM
# -The motor is controlled physically by using the TB6612FNG driver chip and powered by a separate power supply module 9V
# -Only use 2 driver wheels for motion, 2 sets of 2 wheels altogether. The drive wheels are positioned in the center of the bot for
#  easier turning

class MotorDriver:
    #TODO replace LEDS with actual motors --> UPDATE L293D chip burned out, replacements ordered
    # Setup motor pins, all wiring go to 3.3v side of BOB to save space on platform

    # Green light = LEFTW
    # Yellow light = RIGHTW
    LEFTW = 17
    RIGHTW = 27
#
#    PWMEN1 =  17
#    DIRFOR1 = 27
#    DIRREV1 = 22
#
#    PWMEN2 = 21
#    DIRFOR2 = 16
#    DIRREV2 = 20

    # 5 main functions to drive the wheels
    # adjusting the dutycycle for the PWM functions will affect the speed, always have the speed be the same for both wheels.
    # in the cases of turning, the drive wheels run in opposite directions to create turning affect, which is just switching power direction on the motors
    def __init__(self):
        self.leftW = PWMLED(self.LEFTW)
        self.rightW = PWMLED(self.RIGHTW)
    # both drive wheels turn in forward direction
    def forward(self):
        self.leftW.pulse(1,1,None,True)
        self.rightW.pulse(1,1,None,True)

    # both drive wheels turn in the backward direction
    def backward(self):
        self.leftW.pulse(0.4, 0.4, None, True)
        self.rightW.pulse(0.4, 0.4, None, True)

    def turnLeft(self, motorL, motorR):
        self.leftW.pulse(1.0, 1.0, None, True)
        self.rightW.off()

    def turnRight(self, motorL, motorR):
        self.rightW.pulse(1.0, 1.0,None, True)
        self.leftW.off()

    def stop(self):
        self.leftW.off()
        self.rightW.off()


# The ServoDriver controls the SG90 micro servo motor. The servo will control the angle the echo sensor is facing. A single servo is used for turning
# the sensor left and right +- 90 degrees in both directions with 0 facing forward.

class ServoDriver:

    # Maintain a clamp within the bounds of the motor pulse capabilities
    MAXPW = 2200
    MINPW = 500

    pin = 25
    h = lgpio.gpiochip_open(0)
    currentPulseW = 1500

    def setPulse(self, us):
        us = max(self.MINPW, min(self.MAXPW, us))
        self.currentPulseW = us
        lgpio.tx_servo(self.h, self.pin, us)

    # Sweep function that slows the roational speed of the servo motor. This is used to make sure the echo sensor can make accurate readings from front, 
    # left, and right directions the number of steps involved in the turns is the main driver for maipulating the speed of the turn.

    def sweep(self,target, steps=100, delay=0.02):
        start = self.currentPulseW
        target = max(self.MINPW,min(self.MAXPW,target))
        step = (target - start) / steps
        for i in range(steps + 1):
            us = int(start + step * i)
            self.setPulse(us)
            sleep(delay)


    # three main movements of the sensor, instead of constantly moving from one side to the other, have 3 set positions for it to rotate to.
    def centerServo(self,pulse=1500):
        self.sweep(pulse)
        sleep(2)

    def turnLeft(self,pulse=2200):
        self.sweep(pulse)
        sleep(2)

    def turnRight(self,pulse=500):
        self.sweep(pulse)
        sleep(2)




class EchoDriver:

    # setup pins
    TRIG = 23
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # pulse the trigger and receive through echo returns the calc distance
    def pulse(self):
        GPIO.output(self.TRIG, False)
        # send the trigger pulse for 10 microseconds
        GPIO.output(self.TRIG, True)
        sleep(0.0001)
        GPIO.output(self.TRIG, False)

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

    # Distance references for the state machine to work off of throughout the run. The threshold is the minimum distance the bot can be from an obstruction in its line of vision.
    currentDistance = 0
    leftDistance = 0
    rightDistance = 0
    threshold = 20.0

    # States of the machine

    # Instead of having a linear cycle of states from one ot another, there are multiple branches from one state to others in order to cover more scenarios. There is a possibility that while in the sweeping state, all three directions can be less than the threshold or essentially be blocked on all sides.
    # In this case a reverse function will be implemented upon obtaining the new parts.

    idle = State(initial=True) # a default state for the bot to begin in
    sensing = State() # the distance sensing directly in front
    sweeping = State() # read distances from left and right sides to determine open area
    turning = State() # turn the actual bot in the chosen direction
    moving = State() # drive bot in the chosen direction

    # events, conditions are added because of the chances of encountereing obstructions or having an open area. Otherwise soft locks can occur if the conditions are not included, or more states would be needed, adding unecessary states and transitions
    startSensing = idle.to(sensing)
    senseToSweep = sensing.to(sweeping, cond="obstructed")
    senseToMove = sensing.to(moving, cond="all_clear")
    moveToSweep = moving.to(sweeping, cond="obstructed")
    sweepToTurn = sweeping.to(turning, cond="all_clear")
    turnToMove = turning.to(moving, cond="all_clear")
    moveToIdle = moving.to(idle, cond="obstructed")



    # LED displays for different states

    baseLED = PWMLED(26)
    movementLED = PWMLED(13)
    dbWriteLED = PWMLED(19)

    # make objects for physical components within the rolly class

    echoSensor = EchoDriver()
    servo = ServoDriver()
    motors = MotorDriver()

    # temperature sensor
    currentT = 0
    i2c = board.I2C()
    thSensor = adafruit_ahtx0.AHTx0(i2c)


    # transition functions between statesHave you changed your career plans? If so, what prompted this change? If not, why have you remained with your original plan?
How has your thinking about your career evolved?
Have you completed any research about your choice of career? How has this impacted your thinking? Have you thought about seeking an advanced degree or certification after earning your undergraduate degree?
Which course outcomes have you achieved so far, and which ones remain?
    # This is where the physical components are to make their changes. These functions are automatically found and ran when the state cycles from one to the next.

    # when entering the idle state, the bot should have the sensor centered
    def on_enter_idle(self):
        if DEBUG:
            print("Entering Idle")
        self.baseLED.on()
    def on_exit_idle(self):
        if DEBUG:
            print("Exiting Idle")
        self.baseLED.off()

    def on_enter_sensing(self):        
        self.baseLED.pulse(1, 1, None, True)
        self.servo.centerServo()
        self.currentDistance = self.echoSensor.pulse()

    def on_exit_sensing(self):
        if DEBUG:
            print("Exit Sensing")
        self.baseLED.off()
    def on_enter_sweeping(self):
        self.baseLED.pulse(0.1,0.1,None,True)
        
        self.servo.turnLeft()
        self.leftDistance = self.echoSensor.pulse()

        self.servo.turnRight()
        self.rightDistance = self.echoSensor.pulse()
        self.currentDistance = max(self.rightDistance, self.leftDistance)
        self.servo.centerServo()

    def on_exit_sweeping(self):
        self.baseLED.off()
    def on_enter_moving(self):
        if DEBUG:
            print("Entering moving Forward")
        self.movementLED.pulse(1, 1, None, True)
        self.motors.forward()
    def on_exit_moving(self):
        if DEBUG:
            print("Exiting Moving Forward")
        self.movementLED.off()
        self.motors.stop()
    def on_enter_turning(self):
        if DEBUG:
            print("Entering a turn")
        self.movementLED.pulse(0.5,0.5,None,True)
        if self.leftDistance > self.rightDistance:
            self.motors.turnLeft()
        else:
            self.motors.turnRight()
        # depending on direction taken eith turn left or turn right
    def on_exit_turning(self):
        if DEBUG:
            print("Exiting a turn")
        self.movementLED.off()
        self.motors.stop()

    # The run is the main loop for the rolly class. The loop is repeated within the main.py but the function calls are not used in main. This encapsulates the robot class and mechanics, making the main file more clean.
    # This run is a series of conditionals that move from one state to the next depending on whether or not the robot has encountered an obstruction in its path.
    def run(self):
        self.update()
        if self.idle.is_active:
            self.send("startSensing")
        elif self.sensing.is_active:
            if self.all_clear():
                self.send("senseToMove")
            if self.obstructed():
                self.send("senseToSweep")
        elif self.sweeping.is_active:
            if self.all_clear():
                self.send("sweepToTurn")
            else:
                print("blocked")
        elif self.turning.is_active:
            if self.all_clear():
                self.send("turnToMove")
        elif self.moving.is_active:
            if self.obstructed():
                self.send("moveToIdle")

    # These conditional callbacks are used as flags to allow the events to occur and move to the next state
    # The update function at the bottom is to make sure that the distance being used is lways up to date with where the robot is.
    def all_clear(self):
        return self.currentDistance > self.threshold
    
    def obstructed(self):
        return self.currentDistance < self.threshold

    def update(self):
        if self.moving.is_active:
            self.currentDistance = self.echoSensor.pulse()
