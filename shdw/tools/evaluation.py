# ===========================================================================
#   evaluation.py -----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.imgtools
import sklearn
import numpy as np
import pandas as pd
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def evaluation_attempt(prediction, truth, log, specifier=None, **kwargs):
    if len(prediction.shape)==2:
        prediction = shdw.tools.imgtools.expand_image_dim(prediction)

    with open(log, 'w+') as f:
        for channel in range(prediction.shape[2]):
            f.write("Classification report for channel '{}' of image '{}'".format(channel, specifier))
            f.write(
                sklearn.metrics.classification_report(
                    prediction[..., channel].reshape(-1, 1), 
                    truth.reshape(-1, 1),
                    **kwargs
                )
            )

class ConfusionMap():

    # https://www.sciencedirect.com/topics/engineering/confusion-matrix

    def __init__(self, labels, index=None):
        self._labels = labels
        self._index = index
        if not index:
            self._index = range(len(self.labels))
        self._confusion_map = np.zeros((len(self._labels), len(self._labels)), dtype=int)
      
    def update(self, pred, truth):
        for r in self._labels:
            truth_r = truth == r
            for c in self._labels:
                pred_c = pred == c
                self._confusion_map[r, c] += np.count_nonzero(
                    np.logical_and(truth_r == pred_c, truth_r)
                ) 
    
    @property
    def confusion_map(self):
        #             ground  vegetation  buildings   water  bridge  clutter
        # ground      212283      588561     385686  400471       0   188856
        # vegetation   57340      392315      29281  314961       0    25680
        # buildings    49565       95952     111132   65534       0    64904
        # water          472       10878        217   70172       0      270
        # bridge           7           7         23       5       0        4
        # clutter       9901       24794      19063   17592       0     9802
        
        # label 'row' is true but label 'column' was (mis)classified
        data = pd.DataFrame(
            self._confusion_map,
            columns=self._index,
            index=self._index)
        return data

    def to_string(self):
        return self.confusion_map.round(3).to_string()

    def __repr__(self):
        return self.to_string()

class EvalLabeledImg:

    def __init__(self, labels, index=None):
        self._labels = labels
        self._index = index
        if not index:
            self._index = range(len(self.labels))
        # tp, fp, tn, fn (p=tp+fp, n=tn,fn)
        self._scores = np.zeros((len(self._labels), 4), dtype=float)
    
    def update(self, pred, truth):
        for l in self._labels:
            l_pred = pred == l
            l_truth = truth == l

            l_truth_and_pred = l_truth==l_pred
            l_truth_not_pred = l_truth!=l_pred
            l_truth_inverted = np.invert(l_truth)
            self._scores[l,0] += np.count_nonzero(
                np.logical_and(l_truth_and_pred, l_truth)) # tp
            self._scores[l,1] += np.count_nonzero(
                np.logical_and(l_truth_not_pred, l_truth)) # fp
            self._scores[l,2] += np.count_nonzero(
                np.logical_and(l_truth_and_pred , l_truth_inverted))  # tn
            self._scores[l,3] += np.count_nonzero(
                np.logical_and(l_truth_not_pred, l_truth_inverted))  # fn


    @property
    def precision(self):
        # positive predicitve value: tp / (tn + fp)
        # Precision is the estimated probability that a randomly selected retrieved document is relevant
        return np.divide(self._scores[:,0], self._scores[:,2] + self._scores[:,1])

    @property
    def recall(self):
        # true positive rate: tp / (tn + fp)
        # Recall is the estimated probability that a randomly selected relevant document is retrieved in a search
        return np.divide(self._scores[:,0], self._scores[:,2] + self._scores[:,3])

    @property
    def selectivity(self):
        # true negative rate: tn / (tn + fp)
        return np.divide(self._scores[:,1], self._scores[:,2] + self._scores[:,3])

    @property
    def acc(self):
        # accuracy: (tp + tn) / (tp + tn + fp + fn)
        num = self._scores[:,0] + self._scores[:,2]
        return np.divide(num, num + self._scores[:,1] + self._scores[:,3])

    @property
    def bacc(self):
        # balanced accuracy: (tpr + tnr) / 2
        return (self.precision + self.selectivity)/2

    @property 
    def f1_score(self):
        # f1_score: 2tp / (2tp + fp + fn)
        return np.divide(2*self._scores[:,0], 2*self._scores[:,0] + self._scores[:,1] + self._scores[:,3])

    @property
    def iou(self):
        # intersect of union: tp / (tp + fp + fn)
        return np.divide(self._scores[:,0], self._scores[:,0] + self._scores[:,1] + self._scores[:,3])       

    @property
    def support(self):
        # support: tp + fp
        return self._scores[:,0] + self._scores[:,1]
        
    @property
    def scores(self):
        data = pd.DataFrame(
            np.stack((self.acc, self.bacc, self.precision, self.recall, self.f1_score, self.iou, self.support)).T,
            columns=["Accuracy", "Balanced Acc", "Precision", "Recall", "F1 Score", "IoU", "Support"],
            index=self._index)
        return data

    def to_string(self):
        return self.scores.round(3).to_string()

    def __repr__(self):
        return self.to_string()

# sklearn.metrics.multilabel_confusion_matrix
# >>> y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
# >>> y_pred = ["ant", "ant", "cat", "cat", "ant", "cat"]
# >>> confusion_matrix(y_true, y_pred, labels=["ant", "bird", "cat"])
# array([[2, 0, 0],
#        [0, 0, 1],
#        [1, 0, 2]])
#>>> y_pred = [1, 1, 0]
# >>> y_true = [1, 1, 1]