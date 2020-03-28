# ===========================================================================
#   regex.py ----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import os
import pathlib
import re

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class ReSearch():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, regex, group):
        self._regex = re.compile(regex)
        self._group = int(group)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------   
    def __call__(self, pattern):
        try:
            result = self._regex.search(pattern).group(self._group)
        except AttributeError:
            result = None
        return result

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class PathCreator():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, path_dir=os.environ.get("TEMP"), path_name="{}", regex=".*", group=0):
        self._dir = pathlib.Path(path_dir)
        if not self._dir.exists():
            self._dir.mkdir(parents=True, exist_ok=True)
        self._name = path_name
        self._regex = ReSearch(regex, group)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __call__(self, path, index=None):
        name = self._name.format(self._regex(pathlib.Path(path).stem))
        if index is not None:
            name = "{}-{}".format(index, self._name.format(self._regex(pathlib.Path(path).stem)))
        return self._dir / name 