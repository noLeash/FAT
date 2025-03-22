from typing import Dict, Any
from models.methods import ibBars, tick
from ib_client import ib_tools
import datetime as dt
import pprint
import pandas as pd
from utils.logger import setup_logging

logger = setup_logging()


# Base Processor Class
class MethodProcessor:
    """Base class for method processing"""
    
    async def process(self, data: Dict[str, Any]) -> Any:
        """Override this in child classes"""
        raise NotImplementedError("Subclasses must implement this method")

# Processing Classes for Each Method


class ArithmeticMeanProcessor(MethodProcessor):
    async def process(self, data: Dict[str, Any]) -> float:
        numbers = data.get("numbers")
        logger.debug(numbers)
        numlist = numbers.split(',')
        floatList = [float(num) for num in numlist]
        logger.debug(numlist)
        mean = sum(floatList) / len(floatList)
        return mean

class CoefficientOfVarianceProcessor(MethodProcessor):
    def process(self, data: Dict[str, Any]) -> float:
        numbers = data.get("numbers", [])
        if not numbers or len(numbers) < 2:
            raise ValueError("At least two numbers are required")
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
        return (variance ** 0.5) / mean if mean else None


class DivDiscountModel(MethodProcessor):
    async def process(self, data: Dict[str, Any]) -> float:
        try:
            next_div = float(data['next_dividend'])
            required_rate = float(data['required_rate'])
            growth_rate = float(data['growth_rate'])
            p0 = round(next_div / (required_rate-growth_rate), 2)
        except Exception as e:
            return e
        return "P0 = $" + str(p0)


class GeometricMeanProcessor(MethodProcessor):
    async def process(self, data: Dict[str, Any]) -> float:
        print("GEOMEAN")
        values = data.get("list", [])
        print(f"GEOMEAN: {values}")
        print(f"type   : {type(values)}")
        if isinstance(values, str):
            values = [float(num.strip(" ")) for num in values.split(",")]
        print(f"GEOMEAN: {values}")
        if not values:
            raise ValueError("Numbers list is required (CSV)")
        
        # Check for invalid negative values
        for value in values:
            if value < 0:
                raise ValueError("All values must be positive")

        product = 1
        for num in values:
            product *= num
        result = product ** (1 / len(values))
        return round(result, 10)
    

class LeveragedReturn(MethodProcessor):
    async def process(self, data: Dict[str, Any]) -> float:
        print(f"lev_retruns received: {data}")
        
        return "Nice Juan"
    
class Schema(MethodProcessor):
    def process(self, data: Dict[str, Any]) -> float:
        print(f"lev_retruns received: {data}")
        
        return ["Nice Schema", data]


    
class ibHPR():
    async def process(self, data: Dict[str, Any]) -> float:
        ibt = ib_tools()
        print(f'Ticker: {data["ticker_symbol"]}')
        print(f'Start : {data["start_date"]}')
        # print(f'End   : {dt.datetime.strptime(data["end_date"], "%Y-%m-%dT%H:%M:%S.%fZ")})')
        bars_requested = ibBars(
            ticker=data["ticker_symbol"],
            start=dt.datetime.strptime(data["start_date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            end=dt.datetime.strptime(data["end_date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            bar_size="1 day",
            bars=[]
        )
        bar_data = await ibt.fetch_bars(symbol=bars_requested.ticker, start_date=bars_requested.start, end_date=bars_requested.end, bar_size=bars_requested.bar_size)
        
        # print("Bardata:")
        # pprint.pp({bar_data})

        for bar in bar_data:
            barData = tick()
            # pprint.pp(bar)
            barData.open = bar["open"]
            barData.high = bar["high"]
            barData.low = bar["low"]
            barData.close = bar["close"]
            barData.volume = bar["volume"]
            barData.time = bar["time"]

            bars_requested.bars.append(barData)

        #TODO: correct to fetch for specific date -> currently it is using the last bar in an 4 M or 1 Y fetch
        pdBars = pd.DataFrame(bars_requested.bars, columns="index")
        print(f"bars requested")
        print(pdBars)
        holding_period_return = bars_requested.bars#float(bars_requested.bars[-1].close) - float(bars_requested.bars[0].close)
        # pprint.pp(bars_requested.bars)

        return f"Buy: {bars_requested.bars[0]}, Sell: {bars_requested.bars[-1]}, holding_period_return: {holding_period_return}"

# Mapping of Methods to Their Processor Classes
METHOD_PROCESSORS: Dict[str, MethodProcessor] = {
    "geometric_mean": GeometricMeanProcessor(),
    "arithmetic_mean": ArithmeticMeanProcessor(),
    "coefficient_of_variance": CoefficientOfVarianceProcessor(),
    "leveraged_returns": LeveragedReturn(),
    "schema_method": Schema(),
    "div_discount_model": DivDiscountModel(),
    "ibkr_holding_period_return": ibHPR()
}