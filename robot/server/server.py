import socket
import threading

HOSTNAME = "127.0.0.1"
PORT = 5000


class Server:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((HOSTNAME, PORT))
            self.sock.listen(5)
            self.frame = None
            self.client_socket = None
        else:
            self.sock = sock

    def start(self):
        self.client_socket, _ = self.sock.accept()
        thread = threading.Thread(target=self.send, args=())
        thread.start()

    def send(self):
        while True:
            try:
                if self.frame is not None:
                    self.client_socket.send(self.frame)
                    self.frame = None
            except socket.timeout:
                break

    def set_frame(self, frame):
        self.frame = frame
