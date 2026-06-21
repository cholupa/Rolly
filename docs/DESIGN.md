---
layout: page
title: Design Enhancement
---

# Overview

## Original Artifact - CS350:Thermostat.py

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

This artifact was included because the thermostat file contained most of the structure for my project. For an embedded system, unless the system itself is overly complex, the actual file structure can be dialed down to a few files. This is especially so for microcontrollers or microcomputers that do not have much on board memory to use. The libraries used have been condensed to serve 4 main functions.
> rolly.py Imports [rolly file](https://github.com/cholupa/Rolly/blob/main/rolly.py)
```
import RPi.GPIO as GPIO

from time import sleep, time

from statemachine import StateMachine, State

import random

```
RPi.GPIO handles all of the peripheral communications, time to control buffers for peripheral activation and deactivation, statemachine to hold the makeup of the machine states, and random for decision. The project now employs an echo sensor and  2 types of motors, DC mini motors and a SG90 servo motor. The echo sensor is attached to the servo in order to get distance readings in 3 directions, left right, and center. Other enhancements include the addition of 4 files, the rolly.py file to hold the actual robot characteristics, a db.py file for the database functions, and client & server files to relay data to another device/computer.

## Outcome
I believe I have met the outcome of using innovative techniques and most certainly tools for a meaningful purpose. I have updated the code to manage the sensors and motors separately which will help in the upcoming algorithmic side of the project. Enclosing the motors and sensors in classes is usually not necessary in an embedded system that has small memory, but by using a microcomputer instead of a microcontroller, I can safely have a few classes without worrying about memory usage. I also encountered trade-offs in the design, both physical and software related that I believe have resulted in the best course of the project. Because this will be a portable device, the activation of the scripts can be done one of 2 ways. The main loop will be able to be run off of boot, or whilst plugged in through the ssh terminal. Using ssh to activate can give live monitoring to the device, where a run from boot can be a primary function when the project is fully functional.
At the beginning of refactoring the code and files, I aimed to use uv astral to help structure the project, which uv did create a clean space to work off of, but I encountered an issue with using it in this system. Some of the packages used require root access to use the hardware (GPIO) pins. UV creates an enclosed environment that prevents the ability to run as root. This is a safety guard and if allowed to reach root, there are conflicts within the core functions that will break the code. In the end I abandoned the use of a packaging system. In a trade-off for neat organization, I employ direct control by running as root to access the packages saved in the system. Once again, as this is a small device, it is not abnormal to structure a project in this fashion. 
