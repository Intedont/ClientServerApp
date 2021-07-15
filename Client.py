import socket
import time


class ClientError(BaseException):
    def __init__(self, error = "Client Error"):
        self.error = error


class Client:
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout

        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.socket.settimeout(timeout)

    def put(self, name, value, timestamp = int(time.time())):
        # print(name + " " + str(value) + " " + str(timestamp))
        self.socket.sendall(("put " + str(name) + " " + str(value) + " " + str(timestamp) + "\n").encode("utf8"))
        response = self.socket.recv(1024)
        if response.decode("utf8").split('\n')[0] == "error":
            raise ClientError

    def get(self, name):
        self.socket.sendall(("get " + name + "\n").encode("utf8"))
        response = self.socket.recv(1024).decode("utf8")
        response = (response[:len(response)-2]).split('\n')
        if response[0] == "ok":
            d = dict()
            values = list()
            for i in range(1, len(response)):
                buf = response[i].split(' ')
                key = buf.pop(0)
                buf.reverse()
                if key in d.keys():
                    d[key].append(buf)
                else:
                    d[key] = list()
                    d[key].append(buf)
            return d
        else:
            raise ClientError

