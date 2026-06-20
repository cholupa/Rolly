Rolly

# Self Assessment(The Overview)

## ARTIFACTS


## ENGINEERING & DESIGN

---
layout: page
title: Enhancement 1 - Thermostat to Robot Systems
---

[<- Back to Home](README.md)

## Overview

This artifact is based on the Thermostat.py file from the Emerging Systems, Architectures,
and Technologies course. The project was built up throughout the course, starting with a
simple LED circuit and ending with a functional thermostat program, completed in April 2026.

## Narrative

The original thermostat project utilized several libraries for software and hardware
communications including I2C, PWM, and basic hardware interrupts via buttons.

This artifact was chosen as the basis for this enhancement because the thermostat file
contained most of the core structure for the current project. For an embedded system,
unless the system is overly complex, the file structure can be kept minimal -- this is
especially true for controllers or microcomputers with limited onboard memory. The libraries
used in the thermostat, particularly those dealing with hardware control, carry over directly
into the current project.

Rather than a straightforward enhancement, this is more of a lateral expansion. The project
now employs multiple sensors and 2 types of motors -- DC mini motors and SG90 servo motors.
The thermostat remains in use, but only for receiving sensor data, which is used alongside
the HCSR04 echo sensor to obtain more accurate distance measurements. Two new files were
also added: rolly.py to hold the robot characteristics, and db.py for database interactions.

## Skills Demonstrated

Enclosing motors and sensors in classes is not always necessary in an embedded system with
limited memory, but by using a microcomputer rather than a microcontroller, this project
can safely utilize classes without memory concerns. The code was updated to manage sensors
and motors separately, setting up a clean structure for the upcoming algorithmic side of
the project.

Physical and software tradeoffs were encountered throughout development. Because this is a
portable device, the main loop can be run either on boot or through an SSH terminal while
plugged in. SSH activation allows live monitoring, while a boot-triggered run serves as
the primary mode once the project is fully functional.

## Tradeoffs and Challenges

At the start of refactoring, uv astral was used to help structure the project. While uv
created a clean workspace, it proved incompatible with this system -- some packages require
root access to use the GPIO pins, and uv's enclosed environment prevents running as root.
Allowing root access within uv also introduced conflicts in core functions that broke the
code. As a result, the packaging system was abandoned in favor of direct control, running
as root to access system-level packages. For a small embedded device, this is a normal and
accepted project structure.

## Code

```python
# Paste your Thermostat.py / Enhancement 1 code here
```

### Original
[The Thermostat Project](https://github.com/cholupa/Rolly/edit/cholupa-NarrativeDocs/Thermostat.py)
### Enhancement
[The Rolly Bot](https://github.com/cholupa/Rolly/edit/cholupa-NarrativeDocs/rolly.py)


## ALGORITHMS & DATASTRUCTURES

### Original

### Enhancement

## DATABASE

### Original
< 
### Enhancement
