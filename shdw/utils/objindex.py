# ===========================================================================
#   objindex.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.utils.index

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class ObjIndex(shdw.utils.index.Index):

    def __init__(self, obj):
        self._obj = obj
        try:
            super(ObjIndex, self).__init__(len(obj))
        except AttributeError:
            print("Object does not have a iterator.")
            raise

    def __call__(self, index=None):
        if not index:
            index = super(ObjIndex, self).__call__(index=index)
            self.next()
        return self._obj[index]

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def next(self):
        index = super(ObjIndex, self).next()
        return self._obj[index]
        
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def last(self):
        index = super(ObjIndex, self).last()
        return self._obj[index]