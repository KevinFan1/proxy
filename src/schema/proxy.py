class Proxy:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def __str__(self):
        return f'{self.host}:{self.port}'

    def to_string(self):
        return self.__str__()
