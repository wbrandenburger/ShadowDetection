# ===========================================================================
#   imgio.py ----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.tools.imgtools

import numpy as np
import PIL
import shutil
import tifffile

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def read_image(path):
    shdw.__init__._logger.debug("[READ] '{}'".format(path))
    
    if str(path).endswith(".tif"):
        return tifffile.imread(path)
    else:
        return np.asarray(PIL.Image.open(path))
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def save_image(dest,  img):
    shdw.__init__._logger.debug("[SAVE] '{}'".format(dest))

    if str(dest).endswith(".tif"):
        tifffile.imwrite(dest, img)
    else:
        PIL.Image.fromarray(img).write(dest)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def copy_image(path,  dest):
    shdw.__init__._logger.debug("[COPY] '{}'".format(dest))
    shutil.copy2(path, dest)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_image(path, spec="image", param_label=dict(), scale=100, show=False):
    img = shdw.tools.imgtools.resize_img(read_image(path), scale)
    if param_label and spec == "label":
        img = shdw.tools.imgtools.labels_to_image(img, param_label)
    if show:
        img = shdw.tools.imgtools.project_data_to_img(img, dtype=np.uint8, factor=255)
    if show:
        img =  shdw.tools.imgtools.stack_image_dim(img)
    return img
