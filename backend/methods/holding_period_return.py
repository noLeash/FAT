

class holding_period_return:
    def __init__(self):
        pass

    def r_from_PV_FV(self, Present_value: float, Future_value: float):
        """Determine the holding period return from the begingin and end of the period"""
        return_val = str(round((((float(Future_value) / float(Present_value)) - 1)*100) , 2 ))+"%"
        
        return return_val