import socket
import atexit
import xml.etree.ElementTree as ET

from .logger import logger

__all__ = ['dbgp']

XML_NAMESPACE = 'urn:debugger_protocol_v1'

class Client:

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

    def close(self):
        self.connection.close()

    def _receive_length(self):
        length = []
        while 1:
            c = self.connection.recv(1)
            if c == b'':
                self.close()
                raise EOFError('Socket Closed')
            if c == b'\x00':
                return int(b''.join(length))
            if c.isdigit():
                length.append(c)

    def _receive_null(self):
        while 1:
            c = self.connection.recv(1)
            if c == b'':
                self.close()
                raise EOFError('Socket Closed')
            if c == b'\x00':
                return

    def _receive_body(self, total_bytes):
        body = []
        while total_bytes > 0:
            receive_buffer = self.connection.recv(total_bytes)
            if receive_buffer == b'':
                self.close()
                raise EOFError('Socket Closed')
            total_bytes -= len(receive_buffer)
            body.append(receive_buffer.decode("utf-8"))
        return ''.join(body)

    def receive_message(self):
        length = self._receive_length()
        body = self._receive_body(length)
        self._receive_null()
        return body

    def send_message(self, message):
        #self.sock.send(cmd + '\0')
        message_length = len(message)
        total_sent = 0
        while total_sent < message_length:
            sent = self.connection.send(bytes(message[total_sent:].encode()))
            if sent == 0:
                raise RuntimeError('Socket connection broken')
            total_sent = total_sent + sent
        sent = self.connection.send(b'\x00')


class Response:

    def __init__(self, raw_response):
        self.text = raw_response
        self.xml = None

    def get(self, key):
        if self.xml is None:
            self.xml = ET.fromstring(self.text)
        return self.xml.get(key)


class __Dbgp:

    def __init__(self):
        atexit.register(self.close)
        self.client = None
        self.is_connected = False
        self.trans_id = 0
        self.language = None
        self.language_version = None
        self.ide_key = None
        self.start_file = None

    def listen(self, port = 9000):
        self.port = port
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(('', self.port))
            listener.listen()
            (connection, address) = listener.accept()
            self.client = Client(connection, address)
            self.start()
        except socket.timeout:
            listener.close()
            self.is_connected = False
            return 'Timed out after waiting for connection'

        self.is_connected = True
        listener.close()
        return 'Established connection from ' + str(self.client.address)

    def close(self):
        if self.client != None:
            try:
                self.client.close()
            finally:
                self.client = None
                self.is_connected = False
            return 'Closed client connection'
        return 'Client connection already closed'

    def start(self):
        response = Response(self.client.receive_message())

        self.language = response.get('language')
        self.language_version = response.get('xdebug:language_version')
        self.ide_key = response.get('idekey')
        self.start_file = response.get('fileuri')

        logger.log('Started and received: language={} version={} idekey={} file={}'.format(
            self.language,
            self.language_version,
            self.ide_key,
            self.start_file,
        ))

    def command(self, command, args=None, response=Response, silent=False):
        if not self.is_connected:
            if silent: return
            raise RuntimeError('Cannot send command while client not connected')

        self.trans_id += 1
        command_line = '{} -i {}'.format(command, str(self.trans_id))
        if args: command_line += ' ' + args

        logger.log('Sending command: ' + command_line)

        self.client.send_message(command_line)
        raw_response = self.client.receive_message()

        logger.log('Got response: ' + raw_response)

        return response(raw_response)

dbgp = __Dbgp()
