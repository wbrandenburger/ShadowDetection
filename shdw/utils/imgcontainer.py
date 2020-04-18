# ===========================================================================
#   imgcontainer.py ---------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.utils.objcontainer

import pathlib
import tifffile
import numpy as np

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class ImgListContainer(list):

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, default_spec="image", load=None, live=False, obj_flag=True, obj_copy=False, log_dir=None, **kwargs):
        self._default_spec = default_spec
        self._load = load
        self._live = live            
        self._obj_flag = obj_flag, 
        self._obj_copy = obj_copy
        self._log_dir = log_dir        

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def append(self, img=np.ndarray(0), path=None, spec=None, live=None, obj_flag=None, obj_copy=None, **kwargs):

        self._live = self._live if live is None else live
        self._obj_flag = self._obj_flag if obj_flag is None else obj_flag
        self._obj_copy = self._obj_copy if obj_copy is None else obj_copy

        spec = self._default_spec if not spec else spec
        super(ImgListContainer, self).append(
            shdw.utils.imgcontainer.ImgContainer(
                img=img,
                path=path,
                spec=spec,
                load=self._load,
                live=self._live, 
                obj_flag=self._obj_flag, 
                obj_copy=self._obj_copy,
                log_dir=self._log_dir
            )
        )

    def spec(self, spec):
        for item in self:
            if item.spec==spec:
                return item

    # @todo[new]: method __repr__

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class ImgContainer(shdw.utils.objcontainer.ObjContainer):
    
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(
            self, 
            img=np.ndarray(0), 
            path=None, 
            spec="image", 
            load=None,
            live=False,
            obj_flag=True, 
            obj_copy=False,
            log_dir=None            
        ):
        super(ImgContainer, self).__init__(obj=img, obj_flag=obj_flag, obj_copy=obj_copy)

        self._path = None
        if path:
            self.path = path

        self._spec = spec
        self._live = live
        self._load = load if load else lambda path, spec: tifffile.imread(path)
     
        self._log_dir = pathlib.Path(log_dir) if log_dir else None

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @property
    def path(self):
        return self._path

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @property
    def log(self):
        return str(pathlib.Path.joinpath(
            self._log_dir, "{}.log".format(pathlib.Path(self.path).stem)
        )) if self._log_dir else None

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @property
    def spec(self):
        return self._spec

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @path.setter
    def path(self, path):
        self.validate_path(path)
        self._path = path

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @spec.setter
    def spec(self, spec):
        self._spec = spec
    
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------  
    @property
    def data(self):
        if not self._obj.size:
            if self._live:
                return self.imread()
            else:
                self.obj = self.imread() 

        return super(ImgContainer, self).data

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def imread(self):
        if self.validate_path(self.path):
            return self._load(self.path, self.spec)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def load(self):
        self.obj = self.imread()

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def validate_path(self, path, raise_error=True):
        if not pathlib.Path(path).is_file():
            raise ValueError("File {} does not exist.".format(path))
        return True

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __eq__(self, spec):
        return True if spec == self._spec else False

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __repr__(self):
        return "{}\n\t<obj: {}>".format(super(ImgContainer, self).__repr__(), self.obj.shape)