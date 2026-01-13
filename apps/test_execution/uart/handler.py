"""UART handler placeholder."""


class UARTHandler:
    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate

    def open(self):
        return f"Opening UART port {self.port} at {self.baud_rate}"

    def close(self):
        return f"Closing UART port {self.port}"

