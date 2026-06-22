---
layout: page
title: Design Enhancement
---

# Design & Engineering

## Original Artifact - CS350:Thermostat.py

![Thermostat](https://github.com/cholupa/Rolly/blob/main/docs/images/ThermostatOriginal.jpg)

> The thermostat build above

The original artifact acting as the basis for this section was the Thermostat.py file from Emerging Systems, Architectures, and Technologies course. The project was a slow build up throughout the course, starting with a simple LED circuit to a functional thermostat program. This was created recently this year in April 2026 in the previous term. The project utilized different libraries for software and hardware communications including I2C, PWM, and basic hardware interrupts via buttons. 

> States of the machine

```python
class TemperatureMachine(StateMachine):
    #A state machine designed to manage our thermostat

    ##
    ## Define the three states for our machine.
    ##
    ##  off - nothing lit up
    ##  red - only red LED fading in and out
    ##  blue - only blue LED fading in and out
    ##
    off = State(initial = True)
    heat = State()
    cool = State()
```
## Enhancement
[A first time soldering](docs/images/solder1.jpg)

> A necessity to solder after a chip burn out, my first time.

[Attempt # 2](docs/images/solder2.jpg)

> The second round came out a little bit better.


This artifact was included because the thermostat file contained most of the structure for my project. For an embedded system, unless the system itself is overly complex, the actual file structure can be dialed down to a few files. This is especially so for microcontrollers or microcomputers that do not have much on board memory to use. The libraries used have been condensed to serve 4 main functions.

RPi.GPIO handles all of the peripheral communications, time to control buffers for peripheral activation and deactivation, statemachine to hold the makeup of the machine states, and random for decision. The project now employs an echo sensor and  2 types of motors, DC mini motors and a SG90 servo motor. The echo sensor is attached to the servo in order to get distance readings in 3 directions, left right, and center. Other enhancements include the addition of 4 files, the rolly.py file to hold the actual robot characteristics, a db.py file for the database functions, and client & server files to relay data to another device/computer.

> [rolly file](https://github.com/cholupa/Rolly/blob/main/rolly.py)

### The Imports
```python
import RPi.GPIO as GPIO

from time import sleep, time

from statemachine import StateMachine, State

import random

```

### The classes

```python

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

class ServoDriver:


    # Maintain within the bounds duty cycle capabilities
    MAXDC = 12
    CENTERD = 7
    MINDC = 2
    FREQ = 50
    pin = 25
    servo = None

class EchoDriver:

    # setup pins
    TRIG = 23
    ECHO = 24
    TIMEOUTDISTANCE = 200

class Rolly(StateMachine):
    
    currentDistance = 0
    leftDistance = 0
    rightDistance = 0
    turn = None
    # Able variables are to tell if a direction is valid or not
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

```




## Outcome of the enhancement

I believe I have met the outcome of using innovative techniques and most certainly tools for a meaningful purpose. I have updated the code to manage the sensors and motors separately, maintaining a separation of concerns. Enclosing the motors and sensors in classes is usually not necessary in an embedded system that has small memory, but by using a microcomputer instead of a microcontroller, memory capacity is not an issue, with the Rpi4 B containing 4GB of RAM.

>Mem: 3.7Gi       used: 314Mi       free: 3.1Gi       shared: 3.2Mi       buff/cache: 435Mi       available: 3.4Gi


There were tradeoffs in the design such as what peripherals to include compared to space available. There are no hardware interrupts and instead interrupts are managed by the RPi.GPIO library and the OS. Hardware interrupts are preferred over software because of possible timing conflicts in peripheral signaling. 
At the beginning of refactoring the code and files, I aimed to use uv astral to help structure the project, which uv did create a clean space to work off of, but I encountered an issue with using it in this system. Some of the packages used require root access to use the hardware (GPIO) pins. UV creates an enclosed environment that prevents the ability to run as root. This is a safety guard and if allowed to reach root, there are conflicts within the core functions that will break the code. In the end I abandoned the use of a packaging system. In a trade-off for neat organization, I employ direct control by running as root to access the packages saved in the system. Once again, as this is a small device, it is not abnormal to structure a project in this fashion.
Another satisfied outcome is security of the project. There is only a single user that is able to connect through ssh login, providing simple security.
