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
# Rolly is a composite of the driver classes to make the full FSM
#
#
#
#
#
#UPDATES: Button class removed, runs begin from computer through ssh connection, 
#
#####################


import RPi.GPIO as GPIO


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
#GPIO.setmode(GPIO.BOARD)

# -MotorDriver class controls the DC motors for wheel movements using PWM
# -The motor is controlled physically by using the L293D driver chip and powered by a separate power supply module 9V
# -Only use 2 driver wheels for motion, 3 sets of wheels altogether. The drive wheels are positioned in the center of the bot for
#  easier turning

class MotorDriver:
    #TODO replace LEDS with actual motors --> UPDATE L293D chip burned out, replacements ordered
    # Setup motor pins, all wiring go to 3.3v side of BOB to save space on platform
    #
    # Motor driver
    # TB6612FNG
    #L-R
    # VM-----PWMA-4
    # VCC-----A1N2-17
    # GND-----A1N1-27
    # A01-----STBY-22
    # A02-----B1N1-5
    # B02-----B1N2-6
    # B01-----PWMB-13
    # GND-----GND
    #
    # 
    #
    #
    #
    #
    #

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

    def turnLeft(self):
        self.leftW.pulse(1.0, 1.0, None, True)
        self.rightW.off()

    def turnRight(self):
        self.rightW.pulse(1.0, 1.0,None, True)
        self.leftW.off()

    def stop(self):
        self.leftW.off()
        self.rightW.off()


# The ServoDriver controls the SG90 micro servo motor. The servo will control the angle the echo sensor is facing. A single servo is used for turning
# the sensor left and right +- 90 degrees in both directions with 0 facing forward.

class ServoDriver:

#    use Rpi.GPIO

    # Maintain a clamp within the bounds of the motor pulse capabilities
    MAXP = 2000
    CENTERP = 1500
    MINPW = 1000
    currentDC = 0

    MINDC = 2
    MAXDC = 12

    pin = 25
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)
    servo.start(0)
    sleep(2)

    #h = lgpio.gpiochip_open(0)
    #currentPulseW = 1500

    def setPulse(self):
        #lgpio.tx_pwm(self.h, self.pin, 50, 10,pulse_offset=0, pulse_cycles=0)
        self.servo.ChangeDutyCycle(self.currentDC)


    def sweep(self,target):
        self.servo.ChangeDutyCycle(target)
        sleep(1)
        self.servo.ChangeDutyCycle(0)


    def centerServo(self,duty=7):
        self.sweep(duty)
        sleep(2)

    def turnLeft(self,duty=12):
        self.sweep(duty)
        sleep(2)

    def turnRight(self, duty=2):
        self.sweep(duty)
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

        return distance


# The Rolly class is the controller for all physical components
# controls the statemachine mechanics


class Rolly(StateMachine):

    
    currentDistance = 0
    leftDistance = 0
    rightDistance = 0
    direction = 0
    threshold = 20.0

    currentAction = {}

    # States of the machine
    idle = State(initial=True) # a default state for the bot to begin in
    sensing = State() # the distance sensing directly in front
    sweeping = State() # read distances from left and right sides to determine open area
    turning = State() # turn the actual bot in the chosen direction
    moving = State() # drive bot in the chosen direction

    # events
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





    # instance all physical components within the rolly class

    echoSensor = EchoDriver()
    servo = ServoDriver()
    motors = MotorDriver()

    # temperature sensor
    currentT = 0
    i2c = board.I2C()
    thSensor = adafruit_ahtx0.AHTx0(i2c)

    def packAction(self):
        #self.currentAction['distance'] = self.currentDistance
        if self.leftDistance > self.rightDistance:
            self.direction = -90
        elif self.leftDistance < self.rightDistance:
            self.direction = 90
        elif self.currentDistance > self.threshold:
            self.direction = 0
        return self.direction, self.currentDistance



    # transition functions between states
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
    
    def run(self):
        self.update()
        if self.idle.is_active:
            self.send("startSensing")
        elif self.sensing.is_active:
            if self.all_clear():
                self.send("senseToMove")
            elif self.obstructed():
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


    def all_clear(self):
        return self.currentDistance > self.threshold
    
    def obstructed(self):
        return self.currentDistance < self.threshold

    def update(self):
        if self.moving.is_active:
            self.currentDistance = self.echoSensor.pulse()
