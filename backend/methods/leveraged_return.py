from dataclasses import dataclass
from app.helpers import validator

@dataclass
class leveraged_return_input:
    equity_cash: float = None
    equity_pct: float = None
    return_pct: float = None
    return_cash: float = None # aux compute
    debt_cash: float = None
    debt_pct: float = None # aux computek
    debt_rate: float = None
    leveraged_return: float = None
    purchase_price: float = None

class leveraged_return:

    def __init__(self):
        # print(input)
        pass    
    
    def leveraged_return(self, Purchase_price: int, Amount_Borrowed: float, Debt_Rate: float, Final_value: float) -> float:
        """leverage return calcuaiton
        
        Keyword arguments:
        argument -- uses self.data
        Return: leveraged return as 0.02 = 2%
        """
        try:
            data = leveraged_return_input()        
            data.debt_cash = float(Amount_Borrowed)
            data.purchase_price = float(Purchase_price)
            data.purchase_price = float(Purchase_price)
            data.equity_cash = float(Final_value)
            data.return_pct =  data.equity_cash / data.purchase_price
            data.debt_rate = float(Debt_Rate)
            data.debt_pct = data.debt_cash / data.purchase_price
            data.leveraged_return = (float(data.return_pct * data.purchase_price) - (data.debt_cash * data.debt_rate)) / float(data.equity_cash)

            return data
        except Exception as e:
            return f"Value Error: {e}"

    def leveraged_return_series(self):
        # series = []
        # range = .1 * self.data.equity_cash
        # mylist = np.linspace(0, 80, range)
        # print(mylist)
        pass
        

# initiate data class 
data = leveraged_return_input()
