import math
import numpy as np



# plt.style.use('seaborn')
# plt.rcParams['figure.figsize'] = (12, 8)

def welford(x_array):
    k = 0 
    M = 0
    S = 0
    for x in x_array:
        k += 1
        Mnext = M + (x - M) / k
        S = S + (x - M)*(x - Mnext)
        M = Mnext
    return (M, S/(k-1))

class Welford(object):
    """ Implements Welford's algorithm for computing a running mean
    and standard deviation as described at: 
        http://www.johndcook.com/standard_deviation.html
    can take single values or iterables
    Properties:
        mean    - returns the mean
        std     - returns the std
        meanfull- returns the mean and std of the mean
    Usage:
        >>> foo = Welford()
        >>> foo(range(100))
        >>> foo
        <Welford: 49.5 +- 29.0114919759>
        >>> foo([1]*1000)
        >>> foo
        <Welford: 5.40909090909 +- 16.4437417146>
        >>> foo.mean
        5.409090909090906
        >>> foo.std
        16.44374171455467
        >>> foo.meanfull
        (5.409090909090906, 0.4957974674244838)
    """

    def __init__(self,lst=None, num=1, mean=0, std=0):
        self._num = num
        self._mean = mean
        self._std = math.pow(std, 2)*(num-1)
        
        self.__call__(lst)

    @property
    def num(self):
        return self._num    

    @property
    def mean(self):
        return self._mean

    @property
    def std(self):
        if self._num==1:
            return 0
        return math.sqrt(self._std/(self._num-1))

    @property
    def meanfull(self):
        return self._mean, self._std/math.sqrt(self._num)
    
    @property
    def ss(self):
        return self._mean, self._std/math.sqrt(self._num)

    def update(self, lst):
        if lst is None:
            return
        if hasattr(lst, "__iter__"):
            for x in lst:
                self.update_welford(x)
        else:
            self.update_welford(lst)

    def update_welford(self, x):
        if x is None:
            return
        new_mean = self._mean + (x - self._mean)*1./self._num
        new_std = self._std + (x - self._mean)*(x - new_mean)
        self._num += 1
        self._mean, self._std = new_mean, new_std

    def consume(self,lst):
        if isinstance(lst, np.ndarray):
            npfunc = np.vectorize(self.update)
            npfunc(lst)
        else:
            lst = iter(lst)
            for x in lst:
                self.update(x)

    def __call__(self,x):
        if hasattr(x,"__iter__"):
            self.consume(x)
        else:
            self.update(x)

    def __repr__(self):
        return "<Stats: {} +- {}>".format(self.mean, self.std)


