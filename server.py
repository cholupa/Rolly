#---SERVER---#
# The server file to run on a local computer.
# The server receives the movement data from the client and uses it to command the turtle object to draw the path on screen.
# use a queue stack to contain the incoming data to ensure that the steps are recorded in order

import socket
import turtle
import threading
import struct
import queue

HOST = '0.0.0.0'
PORT = 5000
# restrict incoming to packet to 8 bytes
BYTES = struct.calcsize('ii')
# queue stack for the packets to draw with
drawQueue = queue.Queue()
# turtle components
turtle.setup(width=800, height=800)
ttWindow = turtle.Screen()
ttWindow.title("Rolly Pathways")
ttWindow.bgcolor("green")
ttWindow.tracer(0)
# the turtle
tt = turtle.Turtle()
tt.speed(5)
tt.color("brown")
tt.shape("turtle")
tt.penup()
tt.goto(0,0)
tt.pendown()
# labeler
labeler = turtle.Turtle()
labeler.hideturtle()
labeler.penup()
labeler.color("yellow")

stepCount = 0

def startServing():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen()
            print(f"Listening on port {PORT}..")
            while True:
                connection, address = sock.accept()
                with connection:
                    print(f"Connected: {address}")
                    while True:
                        data = connection.recv(BYTES)
                        if not data:
                            print("No Packet")
                            break
                        packet = struct.unpack( 'ii', data)[0:]
                        drawQueue.put(packet)
                        print(f"Step received - distance: {packet[0]} turn: {packet[1]}")
                        
    finally:
        print("Exiting..")

server_thread = threading.Thread(target=startServing)
server_thread.daemon = True
server_thread.start()

def processQueue():
    while not drawQueue.empty():
        packet = drawQueue.get()
        draw(tt, labeler, packet)
        ttWindow.update()
    ttWindow.ontimer(processQueue, 100)


def draw(turtleobj,labelobj, movement):
    global stepCount
    distance, turn = movement
    stepCount += 1

    if turn > 0:
        turtleobj.right(turn)
    elif turn < 0:
        turtleobj.left(turn)
    turtleobj.forward(distance)

    labelobj.goto(turtleobj.position())
    labelobj.write(str(stepCount), align="left", font=("Monospace", 10, "normal"))

processQueue()
turtle.mainloop()

