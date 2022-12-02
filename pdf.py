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
        InterpolatedUnivariateSpline.__init__(self,x,y)
        ycdf = np.array([self.integral(x[0],xcdf)/self.integral(x[0],x[-1]) for xcdf in x])#The spline class has a integral method. We are using list comprehension and normalizing for good measure
        self.cdf = InterpolatedUnivariateSpline(x,ycdf)
        xppf, ippf = np.unique(ycdf, return_index=True) #switch x with y to invert the cdf, while only filtering unique values (injective) and ordering
        yppf = x[ippf] #switch x with y to invert the cdf
        self.ppf = InterpolatedUnivariateSpline(xppf,yppf)

    def __call__(self,x):
        """Function for when the pdf object is called"""
        return InterpolatedUnivariateSpline.__call__(self,x)

    def probinterv(self,x1,x2):
        """Returns the probability of the outcome to be between x1 and x2"""
        return self.cdf(x2)-self.cdf(x1)

    def rng(self,size = 10000):
        """Throws a random number distributed according to the pdf"""
        return self.ppf(np.random.uniform(x[0],x[-1],n))



if __name__ == '__main__':
    x = np.linspace(0,10,30)
    y = np.abs(np.exp(-x))
    pdf = ProbabilityDensityFunction(x,y)
    plt.plot(x,y,'ro')
    plt.plot(x,pdf(x))
    plt.plot(x,pdf.cdf(x))
    randoms = plt.hist(pdf.rng(10000),100,(x[0],x[-1]), density=True) #density normalizes the hist
    #plt.plot(randoms)
    #indexes = (0,1,2,4,7,9.9)
    print(f'Integral is = {pdf.probinterv(0,5)}')
    plt.show()
