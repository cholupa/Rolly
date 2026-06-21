Rolly

# The Assessment

## Learned Skills

  The coursework I have completed throughout this program has given me a good foundation in a few areas of Computer Sciences. First and foremost is organization and planning. This is a skill that is paramount to good and clean programming. Organization deals with your project structure like a typical layout of your files. What sticks out more to me is what the project really needs to contain in order to be functional.

> The Travlr Web Application Tree
```
├── app_admin
├── app_api
├── app.js
├── app_server
├── bin
├── css
├── data
├── node_modules
├── package.json
├── package-lock.json
├── public
└── README.md
```
  Comparing the structure above and below, it is clear that understanding a proper structure will make the development process much more smooth and easier to handle as the project becomes more complex. The above tree is the high level view of a Javascript based web application. Below is the project tree of the Rolly Bot project. Both are suitable for their needs but built very differently. Where a web application requires multiple layers from server access to end user interface, an embedded project like the Rolly Bot tree it is in fact a better practice to keep the system less dense and bulky.

> Rolly Bot
```
.
├── client.py
├── db.py
├── main.py
├── Models
├── rolly.py
├── server.py
└── Thermostat.py
```
  Scripting is involved in almost all aspects of Computer Science and through this program I have learned many languages and the syntaxes that go along with them. Some are better than others, but all follow a baseline flow. Understanding this notion is what makes leaning into new technologies and frameworks easier to get used to. This means that I can learn any framework, given time to read up on it. That is one aspect that the program has taught me.

  ## Programming Topics

*Collaboration with a team*

  Many of the projects within the courses were solo projects, but there was much involvement from other students via discussion posts. These were general discussions on code struggles and problem solving. This is the closest thing to a team based environment with the program. A general concept of teamwork in the field is to understand the division of work within a greater project. Knowing what your task is and not working outside of your scope will help complete a project in a more efficient manner. In this capstone, there was not an actual team environment, but there was much research in its development, requiring reading from outside sources such as posts on StackOverflow and tutorials on library documentation. This research delved into multiple disciplines, including electrical engineering and computer engineering.

*Stakeholder Values*
  
One of the most important things in code development is making sure that you are making a product that is in line with the specifications of the stakeholders. This was made apparent in every project. A mockup of a customer that would have predefined necessities in the programs we created. Functional and technical requirements are a good guide to begin a project with and tailor throughout the development process. Whenever I step into a project, I first think about the requirements and plan the steps to reach those targets.

*Data Structures and Database*

Data structures and algorithms were introduced early on in the program and were continuously built upon in every course. Data structures are the building blocks of a program and algorithms are the methods to manipulate the structures. An example of this was the Android inventory application. A simple application to add an item with a quantity and the ability to change the quantity and delete the item. The item itself is part of the structure that is built from the data in the database. The algorithms involved updated the UI to display properly, managed the communication between the UI and database, and provided security for login schemes. Databases are used in almost every application. Learning about the different types of databases through the course work showed that they also have different purposes. Depending on the application, it may be better to use a SQL based database when you need relations between data sets, where if you want more flexibility and do not require relations between sets, a non relational database like MongoDb is a typical choice to use. They all follow the basic CRUD methods, but are used in different circumstances based on requirements given. 

*Security*

Security often isn’t the first thing you think about in development but it should always have some part in the cycle. Security was not a focus in the courses, but there were always at least simple code blocks that restricted injections which is a frontline defense in coding. Certificate generation and encryption were implemented in the CS305:Software Security course. Learning the basics of certificate generation through the terminal gave insight on where to begin with creating secure code.

*Engineering*

Software engineering is one of the main facets of Computer Science and was implemented throughout the coursework. One of the first things we learned about is the software development life cycle, where you plan, design, build, test, and maintain. This cycle is neverending and will always need improvements, and is no exception to my coursework. The cycle encompasses all of the other topics previously discussed. The following sections will introduce and show how these understanding turned a Raspberry Pi into a functioning robot.


# Introdution to Rolly

The primary artifact referenced throughout this project is a thermostat state machine that reads a temperature from an attached sensor. This was a project from the course CS350: *Emerging Systems, Architectures & Technologies*. Button inputs set a target temperature and change the state to cool, heat or off and manipulate LEDs as an output for a user to tell what is currently happening within the state. This was written in Python and is the basis for the design and data structure categories of the enhancements. The database category did not have any previous artifact and was built from the ground up. Instead of working on separate projects to complete the enhancements, they are combined into a singular project that satisfies all categories. This is the Rolly project. Rolly is an autonomous robot that moves in a direction, senses obstructions, and moves to a new valid direction. The thermostat artifact acts as the foundation for the hardware and structure, and the database layer records the robot actions.

## **ARTIFACTS**

### ENGINEERING & DESIGN

[Go to Engineering & Design Page](DESIGN.md)


## ALGORITHMS & DATASTRUCTURES
[Go to Algorithms & Datastructures](ALGORITHM.md)
### Original

### Enhancement

## DATABASE
[Go to Database](DATABASE.md)
### Original

### Enhancement
