# ===========================================================================
#   regex.py ----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import os
import pathlib
import re

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_value(obj, key, default=None):
    try:
        if key in obj.keys():
            return obj[key]
    except KeyError:
        pass
    return default

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def to_list(*args):
    return (x if isinstance(x, list) or x is None else [x] for x in args)

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class Folder():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self):
        pass

    def set_folder(self, path_dir, path_name=None, ext=None, parents=True, exist_ok=True):
        path_dir_list = path_dir if isinstance(path_dir, list) else [path_dir]

        path = pathlib.Path(path_dir_list[0])
        for dir_idx, dir_part in enumerate(path_dir_list):
            if dir_idx > 0:
                path = pathlib.Path.joinpath(path, dir_part)
        
        path.mkdir(parents=parents, exist_ok=exist_ok)

        if path_name is None:
            return str(path)
            
        path_name = path_name if isinstance(path_name, list) else [path_name]
        path = str(pathlib.Path.joinpath(path, "".join(path_name)))

        if ext is None:
            return path  
        return "".join([path,ext])

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class ReSearch():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, regex=".*", group=0):
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
    def __init__(self, path_dir=os.environ.get("TEMP"), path_name="{}", ext="", regex=[".*", 0]):
        self._dir = pathlib.Path(path_dir)
        if not self._dir.exists():
            self._dir.mkdir(parents=True, exist_ok=True)
        self._name = path_name
        self._regex = ReSearch(*regex)
        self._ext=ext

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def set_ext(self, ext):
        self._ext = ext

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __call__(self, path, prefix=None, path_dir=None, ext=None, **kwargs):
        if path_dir is None:
            path_dir = self._dir
        else:
            path_dir = pathlib.Path(path_dir)

        name = self._name.format(self._regex(pathlib.Path(path).stem))
        if prefix is not None:
            name = "{}-{}".format(prefix, self._name.format(self._regex(pathlib.Path(path).stem)))

        if ext is None:
            ext = self._ext
            
        name = "".join([name, ext])
        return str(pathlib.Path.joinpath(path_dir, name))