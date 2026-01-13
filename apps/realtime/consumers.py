import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TestRunConsumer(AsyncWebsocketConsumer):
    """Minimal consumer for streaming test run updates (placeholder)."""

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=json.dumps({"echo": text_data}))

