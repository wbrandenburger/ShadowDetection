# ===========================================================================
#   dictparser.py -----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.debug.exceptions

from collections.abc import MutableMapping
import re

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class DictParser(MutableMapping):

    # https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/

    def __init__(self, data=()):
        self.mapping = {}
        self.update(data)

        self._regex_interpolation = re.compile("%\((.*)\)s")

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        del self.mapping[key]

    def __setitem__(self, key, value):
        if key in self:
            del self[self[key]]
        self.mapping[key] = value

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f"{type(self).__name__}({self.mapping})"

    def interpolate(self):
        keys = self.keys()
        for key in keys:
            self.mapping[key] = self.__recursive(self.mapping[key])

    def __recursive(self, value):
        if isinstance(value, str):
            value = self.__replace(value)
            # print("String: '{}'".format(values))
        elif hasattr(value, "__iter__"):
            if isinstance(value, list):
                for count, item in enumerate(value):
                    value[count] = self.__recursive(item)
                # print("List: '{}'".format(values)) 
            else:
                for key in value:
                    value[key] = self.__recursive(value[key])
                # print("Dict: '{}'".format(values)) 
        return value

    def __replace(self, value):
        result = self._regex_interpolation.search(value)
        if hasattr(result, "group"):
            if result.group(1) in self.keys():
                try:
                    value = self.mapping[result.group(1)]
                except KeyError:
                    raise shdw.debug.exceptions.KeyErrorJson(result.group(1))
        
        return value
