---
layout: page
title: Algorithm Enhancement
---
# Algorithms & Data Structure

## Original Artifact - CS350:Thermostat.py

  The algorithms used created in this enhancement are primarily for the motion of the robot. The original artifact was a part of the Thermostat.py file, the state machine. A finite state machine was developed for this project to control what actions the robot is supposed to take dependent on its current location in respect to open spaces.

> Thermostat lighting update
> Link to full file [Thermostat](https://github.com/cholupa/Rolly/blob/main/Thermostat.py)

```python
   def updateLights(self):
        ## Make sure we are comparing temperatures in the correct scale
        ## Reset lights to off
        temp = floor(self.getFahrenheit())
        redLight.off()
        blueLight.off()
    
        ## Verify values for debug purposes
        if(DEBUG):
            print(f"State: {self.current_state_value}")
            print(f"SetPoint: {self.setPoint}")
            print(f"Temp: {temp}")

        # Determine visual identifiers
        # check to see if current temp is greater or equal to set point and set to heat 
        if(temp >= self.setPoint and self.current_state_value == 'heat'):
        #then maintain solid red light
            redLight.on()
        #else if current temp is less than set point and in heat
        elif(temp < self.setPoint and self.current_state_value == 'heat'):
        #pulse red light
            redLight.pulse(1,1,None,True)
        else:
        #otherwise not in heat ensure red light is off
            redLight.off()
        #check if current temp less or equal to set point and in cool
        if(temp <= self.setPoint and self.current_state_value == 'cool'):
        #then maintain solid blue light
            blueLight.on()
        #else if current temp is greater than set point and in cool
        elif(temp > self.setPoint and self.current_state_value == 'cool'):
        #pulse blue light
            blueLight.pulse(1,1,None,True)
        #otherwise not in cool and ensure blue light is off
        else:
            blueLight.off()
```
  Listed above is the main loop of actions based on the current state of the machine. This machine is dependent on the current temperature and setPoint.
  
  The main purpose of this enhancement was to create a new state machine and a way to display the data in  a meaningful way. For the robot, instead of reacting to temperature, the driver for action is reaction to distance. The echo sensor reads distances up to ~800 cm. When the robot rolls to a threshold distance (20cm) then the robot will switch to a state of sweeping. During the sweeping the sensor turns via the servo motor to the left and right, recording a distance each time. From there, if at least 1 side is above the threshold, then it will move in that valid direction. This routine goes on for a predetermined number of steps and finishes the route. These steps are recorded into a dictionary pair, the main data structure of the program and written into the database. This is the primary algorithm for the program.

  > Link to full file [rolly](https://github.com/cholupa/Rolly/blob/main/rolly.py)

  ```python
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
```
The other side of this enhancement was how to display the information from the run. The bot doesn't have a viable way for a display, so I decided to send the data to my local computer using a simple socket server. I selected a client/server section of the application mainly to get more practice in learning about networking. This is especially so with using bare bones libraries like socket in Python. Adding a networking block in the program allows me to use the data gathered from the robot. The Turtle application is the software used to draw the pathways. The server side contains the Turtle program to draw the actions of the robot.

> A basic Python dictionary is used in mapping the data to keys within the database record creation.
> Database file [db](https://github.com/cholupa/Rolly/blob/main/db.py)
```python

    def create(con, pathNum, stepNum, distance, turn, stamp):
        key = f'P{pathNum}:S{stepNum}'
        con.hset(key,mapping={f'step:{stepNum}':stepNum,'distance':distance,'turn':turn, 'timestamp':stamp})
        con.set(f'P{pathNum}:latest', stepNum)
        con.sadd('INDEX', key)
        return con.hgetall(key)

```
![A simple path](https://raw.githubusercontent.com/cholupa/Rolly/main/docs/images/Path1.png)

> A simple path draw from the server file

   There were some hiccups in the physical parts such as the original hobby motors not having enough power to move the weight of the robot without extensive work on gearing the motors. I simply did not have the time for it, and ended up purchasing gearbox motors that can handle it. The second problem was the driving chip to control the motors. The chip ended up burning out and honestly I am not sure why. Online reviews state that it is a common flaw with that specific chip. With the time I had left, I worked on the code I could.
  Stated above were a few of the challenges faced, but the coding in this instance was pretty difficult. It looks simple looking at it now, but thinking about how the robot should behave and react is different compared to putting it in code. I kept experiencing soft locks where the sensor would keep turning even though the distance it was reading was well beyond the threshold. This happened mainly within the state of where it has found an obstacle in front. Once the obstacle is seen, the sweeping state begins and the sensor reads in left and right directions. Even though the readings on both sides were above the threshold it did not leave the sweeping state. To fix this I just set the current distance to the max between left and right, which did kick it back into the full cycle. Right now it is a temporary fix until I can implement a moving backwards function and separate the moving state to moving forwards or backwards. At first I also implemented the bot movements and logic into main, which quickly reverted back into the class itself. Main is going to be solely used for the client server communication and only some logic if necessary for the bot. I have found this is a much more complex project, but it is enjoyable in mixing disciplines. On the data structure side, it is a simple matter of making sure of type conversions and flooring the distance. A lot of my time was spent working on the state algorithm and movements, getting physical parts to work, wiring and rewiring the board. 

## Outcomes

  This enhancement was the greatest challenge, from reworking physical components to refactoring a state machine. The main outcome accomplished from these changes is creating a collaborative environment for audiences by opening the communications through sockets and using the Python Turtle library as a visualization tool. The visualization of the data is accessible for anyone regardless of technical background and the use of sockets makes the program available for other people to receive the data and use for their own purposes. The algorithms used employed best practices with clear naming conventions and clear commenting.
