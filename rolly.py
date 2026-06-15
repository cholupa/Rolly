###----ROLLY----###
# This file is for the actual control of the robot. The classes involved in this files handle all of the physical mechanics
# and main logic causing the robot to move, relay display patterns for the leds, and gathers the sensor data.
# 
# There are 4 classes involved, 3 are components of the robot, with the Rolly class being the container for the components.
# EchoDriver - echo sensor controller
# MotorDriver - dc motors for wheel drives
# ServoDriver - servo motor control to turn the sensor to a set direction
# Rolly - manager of the Driver classes
#####################

# GPIO is the framework to allow use of the peripherals and the GPIO pins.
# sleep is used for signal control to ensure no overlaps or faulty signals.
# time used to record time frames with the echo.
# state machine allows the creation of states and transitions. these states make sure the bot will not move to another event or action unless
# state rules are satisfied.
# random used for decision making in uncertain situations.

import RPi.GPIO as GPIO

from time import sleep, time

from statemachine import StateMachine, State

import random

# set the board mode before everything, otherwise will cause conflicts within the classes.
GPIO.setmode(GPIO.BCM)

# MotorDriver class controls the DC motors for wheel movements using PWM.
# the motor is controlled physically by using the L293D driver chip and powered by a separate power supply module 9V.
# only use 2 driver wheels for motion, 3 sets of wheels altogether. The drive wheels are positioned in the center of the bot for
# easier turning.

class MotorDriver:
    
    # Pin designations

    # TB6612FNG
    # VM-----PWMA-4
    # VCC-----A1N2-17
    # GND-----A1N1-27
    # A01-----STBY-22
    # A02-----B1N1-5
    # B02-----B1N2-6
    # B01-----PWMB-13
    # GND-----GND

    PWMA = 4
    A1N2 = 17
    A1N1 = 27
    STBY = 22
    B1N1 = 5
    B1N2 = 6
    PWMB = 13
    FREQ = 100
    DUTY = 85

    # use 2 hobby dc motors to drive the bot, each independent of each other, this way the bot can turn 360 degrees without moving forward.
    # this class is only for motor movement with 4 basic function, forward, backward, left and right.

    motorA = None
    motorB = None

    pins = [PWMA, A1N2, A1N1, STBY, B1N1, B1N2, PWMB]

   # the setup function determines pin type, motors are only output devices so all pins are set to output and PWM pins must be set to a frequency.
    def setupPins(self):
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self.motorA = GPIO.PWM(self.PWMA, self.FREQ)
        self.motorB = GPIO.PWM(self.PWMB, self.FREQ)
        GPIO.output(self.STBY, GPIO.HIGH)
        self.motorA.start(0)
        self.motorB.start(0)

    # the movement functions set the motorspeed and direction.
    # A and B pins are the direction inputs which for each direction are set to either HIGH or LOW.
    # to get same direction set N# to same value for A and B.
    # turns set the N# for A and B opposite
    def forward(self):
        print("forward")
        GPIO.output(self.A1N2, GPIO.LOW)
        GPIO.output(self.B1N2, GPIO.LOW)
        GPIO.output(self.A1N1, GPIO.HIGH)
        GPIO.output(self.B1N1, GPIO.HIGH)

        self.motorA.ChangeDutyCycle(self.DUTY)
        self.motorB.ChangeDutyCycle(self.DUTY)


    def backward(self):
        GPIO.output(self.A1N1, GPIO.LOW)
        GPIO.output(self.B1N1, GPIO.LOW)

        GPIO.output(self.A1N2, GPIO.HIGH)
        GPIO.output(self.B1N2, GPIO.HIGH)

        self.motorA.ChangeDutyCycle(self.DUTY)
        self.motorB.ChangeDutyCycle(self.DUTY)

    def turnLeft(self):
        
        GPIO.output(self.A1N2, GPIO.LOW)
        GPIO.output(self.B1N2, GPIO.HIGH)
        GPIO.output(self.B1N1, GPIO.LOW)
        GPIO.output(self.A1N1, GPIO.HIGH)

        self.motorA.ChangeDutyCycle(self.DUTY)
        self.motorB.ChangeDutyCycle(self.DUTY)

        sleep(2)

        self.motorA.ChangeDutyCycle(0)
        self.motorB.ChangeDutyCycle(0)

    def turnRight(self):
        GPIO.output(self.A1N2, GPIO.HIGH)
        GPIO.output(self.B1N2, GPIO.LOW)
        GPIO.output(self.B1N1, GPIO.HIGH)
        GPIO.output(self.A1N1, GPIO.LOW)

        self.motorA.ChangeDutyCycle(self.DUTY)
        self.motorB.ChangeDutyCycle(self.DUTY)

        sleep(2)

        self.motorA.ChangeDutyCycle(0)
        self.motorB.ChangeDutyCycle(0)


    def stop(self):
        self.motorA.ChangeDutyCycle(0)
        self.motorB.ChangeDutyCycle(0)



# The ServoDriver controls the SG90 micro servo motor.
# The servo turns in 90 degree increments, making the sensor face eithe straight forward, directly left or directly right
# the sensor left and right +- 90 degrees in both directions with 0 facing forward.

class ServoDriver:


    # Maintain within the bounds duty cycle capabilities
    MAXDC = 12
    CENTERD = 7
    MINDC = 2
    FREQ = 50
    pin = 25
    servo = None

    def setupPins(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, self.FREQ)
        self.servo.start(0)

    # sets sensor to specified position
    def sweep(self,target):
        self.servo.ChangeDutyCycle(target)
        sleep(0.2)
        self.servo.ChangeDutyCycle(0)
    
    # set the sensor straight ahead
    def centerServo(self):
        self.sweep(self.CENTERD)
        sleep(0.2)
    # set sensor 90 to the left
    def turnLeft(self):
        self.sweep(self.MAXDC)
        sleep(0.2)
    # set sensor 90 to the right
    def turnRight(self):
        self.sweep(self.MINDC)
        sleep(0.2)


# the echo driver is only to record the distance from the sensor and return the distance to the bot for decision making
# distance is recorded in centimeters
class EchoDriver:

    # setup pins
    TRIG = 23
    ECHO = 24
    TIMEOUTDISTANCE = 200

    #v = 82 cm/s

    def setupPins(self):
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    # pulse the trigger and receive through echo returns the calc distance
    # pulse width is 10 microseconds per device specs
    # the timeout is a value used to check if the sensor is waiting on an endless echo or none at all
    def pulse(self):
        GPIO.output(self.TRIG, False)
        GPIO.output(self.TRIG, True)
        sleep(0.0001)
        GPIO.output(self.TRIG, False)

        # check for sensor fault 
        timeout = time() + 0.04 
        startTime = time()
        endTime = time()

        while GPIO.input(self.ECHO) == 0:
            startTime = time()
            # waiting for echo to go HIGH, if not, the trigger did not send properly
            if time() > timeout:
                return self.TIMEOUTDISTANCE + 1

        while GPIO.input(self.ECHO) == 1:
            endTime = time()
            # waiting for a reset, if signal stays high then either blocked or signal is stuck
            if time() > timeout:
                return 0

        elapsedTime = endTime - startTime
        return (elapsedTime * 34300) / 2


# The Rolly class is the controller for all physical components

class Rolly(StateMachine):
    
    currentDistance = 0
    leftDistance = 0
    rightDistance = 0
    turn = None
    # Able vairables are to tell if a direction is valid or not
    leftAble = False
    rightAble = False
    # the minimum distance that the robot can travel until it is officially obstructed
    threshold = 20.0
    direction = 0
    # check to see if the step is finished in order to send the path data
    stepReady = False
    LEDFREQ = 80
    # LED pins that pulse for each general function, a base light for program running, moving for when the robot moves, and when there is a write to the database
    BASE = 12
    MOVE = 16
    WRITE = 21

    def __init__(self):
        self.echoSensor = EchoDriver()
        self.servo = ServoDriver()
        self.motors = MotorDriver()

        GPIO.setup(self.BASE, GPIO.OUT)
        GPIO.setup(self.MOVE, GPIO.OUT)
        GPIO.setup(self.WRITE, GPIO.OUT)

        self.setupAll()

        super().__init__()
    

    # States of the machine
    # 5 different states that are transitioned to by defined events below.
    # the robot can only be in one state at a time and must transition via event calls
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

    def setupAll(self):
        self.baseLED = GPIO.PWM(self.BASE, self.LEDFREQ)
        self.movementLED = GPIO.PWM(self.MOVE, self.LEDFREQ)
        self.dbWriteLED = GPIO.PWM(self.WRITE, self.LEDFREQ)
        self.baseLED.start(0)
        self.movementLED.start(0)
        self.dbWriteLED.start(0)
        self.echoSensor.setupPins()
        self.servo.setupPins()
        self.motors.setupPins()
    # TODO add in all device and peripheral checks to make sure ALL are functional
    def test(self):
        testDistance = self.echoSensor.pulse()

    # takes the sensor data for distance around it and decides which direction to take. if multiple options are available, then a random choice will be decided on
    def packAction(self):
        self.rightAble = self.rightDistance > self.threshold
        self.leftAble = self.leftDistance > self.threshold
        
        if self.currentDistance > self.threshold:
            self.direction = 0
            return self.direction, self.currentDistance
        else:
            if self.rightAble and not self.leftAble:
                self.direction = 90
                self.currentDistance = self.rightDistance
            elif not self.rightAble and self.leftAble:
                self.direction = -90
                self.currentDistance = self.leftDistance
            elif self.rightAble and self.leftAble:
                if random.randint(0,1):
                    self.direction = 90
                    self.currentDistance = self.rightDistance
                else:
                    self.direction = -90
                    self.currentDistance = self.leftDistance
            else:
                return None, None

        return self.direction, self.currentDistance
            

    # transition functions between states
    # This is where the physical components are to make their changes. These functions are automatically found and ran when the state cycles from one to the next.

    # when entering the idle state, the bot should have the sensor centered
    def on_enter_idle(self):
        if DEBUG:
            print("Entering Idle")
        self.baseLED.ChangeDutyCycle(60)

    def on_exit_idle(self):
        if DEBUG:
            print("Exiting Idle")
        self.baseLED.ChangeDutyCycle(0)

    def on_enter_sensing(self):        
        self.baseLED.ChangeDutyCycle(5)
        self.servo.centerServo()
        self.currentDistance = self.echoSensor.pulse()

    def on_exit_sensing(self):
        if DEBUG:
            print("Exit Sensing")
        self.baseLED.ChangeDutyCycle(0)
    def on_enter_sweeping(self):
        self.baseLED.ChangeDutyCycle(20)
        self.servo.turnLeft()
        self.leftDistance = self.echoSensor.pulse()

        self.servo.turnRight()
        self.rightDistance = self.echoSensor.pulse()
        self.currentDistance = max(self.rightDistance, self.leftDistance)
        self.servo.centerServo()

    def on_exit_sweeping(self):
        self.baseLED.ChangeDutyCycle(0)

    # when entering a move, continue moving forward until an obstruction is found
    def on_enter_moving(self):
        if DEBUG:
            print("Entering moving Forward")
        self.movementLED.ChangeDutyCycle(40)
        self.motors.forward()
        while True:
            self.currentDistance = self.echoSensor.pulse()
            if self.obstructed():
                self.motors.stop()
                break

    # if the move is finished then the step is finished
    def on_exit_moving(self):
        if DEBUG:
            print("STOPPING")
        self.movementLED.ChangeDutyCycle(0)
        self.stepReady = True
    
    def on_enter_turning(self):
        if DEBUG:
            print("Entering a turn")
        self.movementLED.ChangeDutyCycle(30)
        if self.leftDistance > self.rightDistance:
            self.motors.turnLeft()
        else:
            self.motors.turnRight()
    
    def on_exit_turning(self):
        if DEBUG:
            print("Exiting a turn")
        self.movementLED.ChangeDutyCycle(0)
        self.motors.stop()
    
    # a run is defined by the events the robot goes through and when a condition is met will send the robot to the next state
    def run(self):
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

