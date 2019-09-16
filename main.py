from robot.camera.camera import Camera
from robot.server.server import Server

camera = Camera()
server = Server()
server.start()
while True:
    server.set_frame(camera.read())