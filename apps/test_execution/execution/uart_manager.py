"""UART connection pooling (placeholder)."""


class UARTManager:
    def acquire(self, port: str):
        return f"Acquired UART port {port}"

    def release(self, port: str):
        return f"Released UART port {port}"

