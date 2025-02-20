from ib_async import IB, Stock, util
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

IBKR_IP = os.getenv("IBKR_IP", "127.0.0.1")  # Default to localhost
IBKR_PORT = int(os.getenv("IBKR_PORT", 7497))  # Default port 7497

class IBclient:
    def __init__(self, host=IBKR_IP, port=IBKR_PORT, client_id=6):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False  # Track connection state

    async def connect(self):
        """Connect to IBKR with error handling."""
        try:
            await self.ib.connectAsync(self.host, self.port, self.client_id)
            self.connected = True
            print("✅ Connected to IBKR")
        except Exception as e:
            self.connected = False
            print(f"⚠️ Failed to connect to IBKR: {e}")

    def disconnect(self):
        """Disconnect from IBKR."""
        self.ib.disconnect()
        self.connected = False
        print("🔌 Disconnected from IBKR")

    def is_connected(self):
        """Check if connected to IBKR."""
        return self.connected and self.ib.isConnected()

    async def check_connection(self):
        """Background task to reconnect IBKR if disconnected."""
        while True:
            if not self.is_connected():
                print("⚠️ IBKR Disconnected. Attempting to reconnect...")
                await self.connect()
            await asyncio.sleep(60)  # Check connection every minute

ib_connection = IBclient()


async def run_test():
    await ib_connection.connect()
    print("CONNECTED:", ib_connection.is_connected)



if __name__ == "__main__":
    asyncio.run(run_test())
