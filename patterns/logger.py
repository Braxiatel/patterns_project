from datetime import datetime
from socket import socket


class LoggerSingleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=LoggerSingleton):
    """
    Simple logger to console.
    """

    def __init__(self, name: str):
        self.name = name

    def log(self, text: str):
        now_time = datetime.now()
        print(f'[{self.name}] {now_time} ->', text)


class FileLogger(metaclass=LoggerSingleton):
    """
    Logger into a file
    """
    def __init__(self, name: str, file: str):
        self.name = name
        self.file = file

    def log(self, text):
        with open(self.file, "a", encoding='utf-8') as f:
            now_time = datetime.now()
            f.write(f'[{self.name}] {now_time} -> {text}\n')


class SocketLogger(metaclass=LoggerSingleton):
    """
    Logger to a socket
    """
    def __init__(self, name: str, sock: socket):
        self.name = name
        self.sock = sock

    def log(self, text):
        now_time = datetime.now()
        self.sock.sendall(f'[{self.name}] {now_time} -> {text}\n'.encode('ascii'))
