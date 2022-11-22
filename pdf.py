"""
Assignment 4 of CMEP course : class that throws a pseudo random number distributed according to a given pdf.

"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import InterpolatedUnivariateSpline

class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
    def __init__(self,x,y):
        """Class constructor"""
        super().__init__(self,x,y)
        ycdf = np.array([self.integral(x[0],xcdf) for xcdf in x])#The spline class has a integral method
        self.__cdf = InterpolatedUnivariateSpline(x,ycdf)
        xppf, ippf = np.unique(ycdf, return_index=True) #switch x with y to invert the cdf, while only filtering unique values (injective) and ordering
        yppf = x[ippf] #switch x with y to invert the cdf
        self.__ppf = InterpolatedUnivariateSpline(xppf,yppf)

    def __call__(self,indexes):
        pntlist = [(x[i],y[i]) for i in indexes]
        print('The passed values at corresponding indices are:')
        for cartesian in pntlist: print(f'{(cartesian)}\n')

    


if __name__ == '__main__':
    x = np.linspace(0,100,100)
    y = np.sin(x)
    plt.plot(x,y)
    pdf = ProbabilityDensityFunction(x,y)
    indexes = (0,12,24,45,70,99)
    pdf(indexes)
    plt.show()
