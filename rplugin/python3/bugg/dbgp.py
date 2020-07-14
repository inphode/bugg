import socket
import atexit
import xml.dom.minidom

__all__ = ['dbgp']

class __Dbgp:

    def __init__(self):
        self.client = None
        self.is_connected = False
        atexit.register(self.close)

    def listen(self, port = 9000):
        self.port = port
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(('', self.port))
            listener.listen()
            (self.client, self.address) = listener.accept()
        except socket.timeout:
            listener.close()
            self.is_connected = False
            return 'Timed out after waiting for connection'

        self.is_connected = True
        listener.close()
        return 'Established connection from ' + str(self.address)

    def close(self):
        if self.client != None:
            try:
                self.client.close()
            finally:
                self.client = None
                self.is_connected = False
            return 'Closed client connection'
        return 'Client connection already closed'

dbgp = __Dbgp()
