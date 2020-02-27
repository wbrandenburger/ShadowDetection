# ===========================================================================
#   imagestats.py -----------------------------------------------------------
# ===========================================================================
import numpy as np
import pandas as pd
import math
import shdw.tools.welford
# from multiprocessing import Pool
import tempfile
import scipy.stats as ss
import matplotlib.pyplot as plt

class ImageStats(object):

    def __init__(self, cat=list(), channels=None, path=None):
        # create a dictionary with objects

        if path:
            self.read(path)
        else:
            stats = dict()
            index = range(channels)
            for c in cat:
                a = list()
                for ch in index:
                    a.append(shdw.tools.welford.Welford())
                stats.update({ c : a}) 
            self._stats = pd.DataFrame(stats, columns=stats.keys(), index=index)

        self._stats.columns.name = "Label"
        self._stats.index.name = "Channel"

    def __call__(self, img, label):
        self.update(img, label)

    @property
    def keys(self):
        return self._stats.keys()

    def update(self, img, label):
        img, label =  (self.expand(o) for o in [img, label])
        for c_index, c_data in self._stats.iteritems():
            for r_index, r_data in enumerate(list(c_data)):
                self._stats.iloc[r_index, c_index] = self.get_intensity_of_label(img[...,r_index], label, c_index, r_data)
                print(r_index, c_index, r_data)
        return

    def expand(self, img):
        self.validate(img)
        return np.expand_dims(img, axis=2) if len(img.shape) != 3 else img

    def validate(self, img, raise_error=True):
        if not isinstance(img, np.ndarray):
            if raise_error:
                raise ValueError("Object is not an instance of 'np.ndarray'")
            else:
                return False
        return True

    def get_intensity_of_label(self, img, label, value, stats):
        mask = np.ma.masked_where(label[...,-1] == value, img)
        data_masked = img[mask.mask]
        if data_masked.size!=0:
            stats(data_masked)
        return stats

    @property
    def stats(self):
        return self._stats

    def __repr__(self):
        return "{}".format(self._stats)

    def write(self):
        tmp_obj = tempfile.mkstemp(suffix=".json")
        self._stats.to_json(tmp_obj[1], orient="split")
        return tmp_obj[1]

    def read(self, path):
        tmp_stats = pd.read_json(path, orient="split")
        for c_index, c_data in tmp_stats.iteritems():
            for r_index, r_data in enumerate(list(c_data)):      
                tmp_stats.iloc[r_index,c_index] = shdw.tools.welford.Welford(
                    num = r_data["num"],
                    mean= r_data["mean"], 
                    std = r_data["std"]
                ) 
        self._stats = tmp_stats

    # def iter_stats(self, func=None, *args, **kwargs):
    #     for c, row in self._stats.iteritems():
    #         for r, value in enumerate(list(row)):
                
    def plot_stats(self, index):
        x = np.linspace(0, 255, 256)
        for c_index, c_data in self._stats.iteritems():
            if c_index == index:
                for r_index, r_data in enumerate(list(c_data)):             
                    obj = self._stats.iloc[r_index,c_index]
                    y_pdf = ss.norm.pdf(x, obj.mean, obj.std) 
                    plt.plot(x, y_pdf, label='pdf')
            #     # the normal cdf
            #     if cdf:
            #     y_cdf = ss.norm.cdf(x, self.mean, self.std) * np.max(y_pdf)
            #     plt.plot(x, y_cdf, label='cdf') 

        plt.legend()
        plt.show()

    def get_probability_a(self, pixel):
        result = np.ones((6), dtype=float)
        for c_index, c_data in self._stats.iteritems():
            for r_index, r_data in enumerate(list(c_data)):             
                obj = self._stats.iloc[r_index,c_index]
                result[c_index] += np.log10(ss.norm.pdf(pixel[r_index], obj.mean, obj.std))
        return result


    def get_probability_b(self, pixel):
        result = np.ones((6), dtype=float)
        for c_index, c_data in self._stats.iteritems():
            for r_index, r_data in enumerate(list(c_data)):             
                obj = self._stats.iloc[r_index,c_index]
                result[c_index] += np.log10(self.normpdf(pixel[r_index], obj.mean, obj.std))
        return result
    
    def get_probability_c(self, pixel):
        result = np.zeros((6), dtype=float)

        index = np.NAN
        b = -np.Infinity
        for c_index, c_data in self._stats.iteritems():
            a = 0
            for r_index, r_data in enumerate(list(c_data)):             
                obj = self._stats.iloc[r_index,c_index]
                a += np.log10(self.normpdf(pixel[r_index], obj.mean, obj.std))
            if np.isfinite(a) and a > b:
                b = a
                index = c_index
        #index = np.argmax(result[np.isfinite(result)])/(6.-1.)
        return float(index)/5. if np.isfinite(index) else 0.
    
    def normpdf(self, x, mean, sd):
        var = float(sd)**2
        if var:
            denom = (2*math.pi*var)**.5
            num = math.exp(-(float(x)-float(mean))**2/(2*var))
            return num/denom
        else:
            return 0