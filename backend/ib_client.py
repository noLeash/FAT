from ib_async import IB, Stock, util, Option
import asyncio
import pprint
import os
from dotenv import load_dotenv
import datetime as dt
from models.methods import tick


load_dotenv()

IBKR_IP = os.getenv("IBKR_IP", "127.0.0.1")  # Default to localhost
IBKR_PORT = int(os.getenv("IBKR_PORT", 4001))  # Default port 7497

class IBclient:
    def __init__(self, host=IBKR_IP, port=IBKR_PORT, client_id=8):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False  # Track connection state

    async def connect(self):
        """Connect to IBKR with error handling."""
        if not self.ib.isConnected():
            try:
                await self.ib.connectAsync(self.host, self.port, self.client_id)
                self.connected = True
                print("✅ Connected to IBKR")
            except Exception as e:
                self.connected = False
                print(f"⚠️ Failed to connect to IBKR: {e}")
        else:
            print("🔄 Already connected to IBKR")

    def disconnect(self):
        """Disconnect from IBKR."""
        if self.ib.isConnected():
            self.ib.disconnect()
            self.connected = False
            print("🔌 Disconnected from IBKR")

    def is_connected(self):
        """Check if connected to IBKR."""
        return self.connected and self.ib.isConnected()


class ib_tools:
    def __init__(self):
        self.ib_connection = IBclient()
        # await self.ib_connection.connect()

    async def fetch_adjusted_history(self, symbol: str, start_date: dt.datetime, end_date: dt.datetime, bar_size: str = "1 day"):
        await self.ib_connection.connect()
        contract = Stock(symbol, "SMART", "USD")  # Fix Stock instantiation

        if isinstance(end_date, str):
            end_date = dt.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")

        duration = self.format_time_difference(start_date, end_date)

        end_date_str = end_date.strftime("%Y%m%d %H:%M:%S")  # Fix time formatting
        print(f"Contract: {contract} // Duration:{duration} // End Date Time: {end_date_str}")
        try:
            dividends_data = await self.ib_connection.ib.reqHistoricalDataAsync(contract=contract, endDateTime=end_date_str, durationStr=duration, barSizeSetting=bar_size, whatToShow="ADJUSTED_LAST", useRTH=True)
            formatted_bars = [
                {
                    "time": bar.date,
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "volume": bar.volume
                }
                for bar in dividends_data
            ]
            pprint.pp(formatted_bars)
            self.ib_connection.disconnect()
            return formatted_bars
        except Exception as e:
            print(f"❌ Error fetching adjusted bars: {e}")
            self.ib_connection.disconnect()
            return None

    async def fetch_option_chain(self, symbol):
        await self.ib_connection.connect()
        contract = Stock(symbol, "SMART", "USD")  # Fix Stock instantiation∂

        details = await self.ib_connection.ib.reqContractDetailsAsync(contract=contract)
        self.ib_connection.ib.reqMktData(contract=contract)
        await asyncio.sleep(1)
        print(details[0].contract.conId)
        print(self.ib_connection.ib.ticker(contract=contract))
        self.ib_connection.disconnect()

    async def fetch_bars(self, symbol: str, start_date: dt.datetime, end_date: dt.datetime, bar_size: str = "1 day", formatted_bars: tick = None):
        print(f"symbol: {symbol} // end date: {end_date} // start {start_date}")
        await self.ib_connection.connect()

        contract = Stock(symbol, "SMART", "USD")  # Fix Stock instantiation

        if isinstance(end_date, str):
            end_date = dt.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")

        duration = self.format_time_difference(start_date, end_date)

        end_date_str = end_date.strftime("%Y%m%d %H:%M:%S")  # Fix time formatting

        print(f"📊 Fetching {bar_size} bars for {symbol} for {duration} to {end_date_str}")

        try:
            bars = await self.ib_connection.ib.reqHistoricalDataAsync(
                contract=contract,
                endDateTime=end_date_str,
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow="TRADES",
                useRTH=True,
            )

            formatted_bars = [
                {
                    "time": bar.date,
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "volume": bar.volume
                }
                for bar in bars
            ]
            pprint.pp(formatted_bars)
            dictBars = formatted_bars.model_dump()
            self.ib_connection.disconnect()
            return formatted_bars

        except Exception as e:
            print(f"❌ Error fetching bars: {e}")
            return None

    
    def format_time_difference(self, start_date: dt.datetime, end_date: dt.datetime) -> str:
        delta_days = (end_date - start_date).days

        if delta_days < 30:
            return f"{delta_days} D"
        elif delta_days < 365:
            return f"{(delta_days // 30) + 1} M"
        else:
            return f"{delta_days // 365} Y"


if __name__ == "__main__":
    ibt = ib_tools()
    start_date = dt.datetime(2024, 2, 18)
    end_date = dt.datetime(2024, 2, 22)
    
    loop = asyncio.get_event_loop()

    tasks = [
        ibt.fetch_dividend_history("F")
        # ibt.fetch_bars("AAPL", start_date, end_date, bar_size="1 day")
    ]
    
    loop.run_until_complete(asyncio.gather(*tasks))