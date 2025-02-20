import numpy as np
from decimal import Decimal
from scipy.stats import gmean

class means:
    def __init__(self):
        pass

    def arithmetic(self, values: list):
        print(f"Values: {values}")
        print(f"Count: {len(values)}")
        average = float(sum(values)/len(values))
        # print(f"Average: {average}")
        
        return average

    def geometric(self, values: list):
        """This Method Returns the Geometirc Mean"""
        try:
            data_list = []
            for value in values:
                if value < 0:
                    return "Value Error - All Values must be greater than zero"
                else:
                    data_list.append(value)
                    
            sipy_gmean = gmean(data_list)
            # print(f"py gmean: {py_gmean}")
            # print(f"np gmean: {np_gmean}")
            # print(f"sipy gme: {sipy_gmean}")

            # This method returns the most accurate unit test
            # decimal_gmean = Decimal(1)
            # for val in values:
            #     decimal_gmean *= Decimal(val)
            # decimal_gmean = decimal_gmean ** (Decimal(1) / len(values))

            # decimal_gmean = float(round(decimal_gmean, 3))
            # print(f"deci gme: {sipy_gmean}")
            return sipy_gmean
        except Exception as e:
            return f"Value Error: error - {e}"
    
        
    
    def harmonic(self, values: list):
        """This method retuns the harmonic mean.\nIt will only accept positive floats"""
        try:
            print(f"Values: {values}")
            print(f"Count: {len(values)}")
            harmonic_mean = (len(values) / sum(1 / value for value in values))
            # harmonic_mean = len(values)/(sum(sum ))
            return harmonic_mean
        except ValueError as e:
            return f"Value Error: {e}"
    
    def time_weighed_return(self, values: list):
        pass


if __name__ == "__main__":
    values = [22.29, 5]
#     values = [value *.05 for value in values]
    means = means()
    # print(f"Average:   {means.arithmetic(values)}")
    print(f"Geometric: {means.geometric(values)}")
#     print(f"Harmonic: {means.harmonic(values)}")