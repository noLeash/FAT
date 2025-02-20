from app.models.models import SingleAxisListModel



class variance:
    def __init__(self):
        pass

    def Coefficent_of_Variation(self, Observations: SingleAxisListModel):
        """ratio for relative comparison

        As standard deviation returns a value in the same unit of 
        measurement as the the observations, the Coefficent of Varaiation
        becomes helpful when needing to compare standard deviations 
        of two datasets of unrealted observations.
        """
        return Observations

    def standard_deviation(self, Observations: SingleAxisListModel):
        """Calculates the standard deviation of a list

        A measurement that squares the sum of the total deviations 
        squared divided by the number of deviations minus one to 
        represent the 'spot' int the data
        
        Standard deviation is more easily interpreted than variance 
        because standard deviation uses the same units of measurement
        as the observations
        """

        # standard deviation =
        
        # sqrt of (
        #     square (
        #         the sum of (
        #             observation - the arithmetic mean of the observations
        #         )
        #     )
        #     /
        #     (
        #         number of observations - the one observation that we are accounting for
        #     )
        # )
    
        pass

    def target_semideviation(self, Observations: SingleAxisListModel, Target_Value: float):
        """A measure of downside risk calculated as the sqrt of the aveage of the squared deviations"""
        # target_ds_dev = 
        # 
        # sqrt of ( 
        #   the sum of ( 
        #       if observation <= target value:
        #           (observation(X_n) - target deviaton(B)) squared 
        #   ) / 
        #   by the total number of obseravations - 1 (because this accounts for our spot in the caluclation) 
        # )
        
        return 
