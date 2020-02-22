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
    shdw.__init__._logger.debug("Read image '{}'".format(path))
    
    if str(path).endswith(".tif"):
        return tifffile.imread(path)
    else:
        return np.asarray(PIL.Image.open(path))
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def save_image(dest,  img):
    shdw.__init__._logger.debug("Save img to '{}'".format(dest))

    if str(dest).endswith(".tif"):
        tifffile.imwrite(dest, img)
    else:
        PIL.Image.fromarray(img).write(dest)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def copy_image(path,  dest):
    shdw.__init__._logger.debug("Copy img to '{}'".format(dest))
    shutil.copy2(path, dest)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_image(path, spec="image", labels=dict(), msi=[0,1,2], scale=100):
    
    img = shdw.tools.imgtools.resize_img(read_image(path), scale)

    if spec == "label":
        img = shdw.tools.imgtools.labels_to_image(img, labels)

    if spec in ["label", "height", "msi"]:
        img = shdw.tools.imgtools.project_data_to_img(img)

    if spec == "msi" and msi:
        img = np.stack((img[:,:,msi[0][0]], img[:,:,msi[0][1]], img[:,:,msi[0][2]]), axis=2)

    img =  shdw.tools.imgtools.stack_image_dim(img)

    return img
    
# @todo[new]: function for determining unique tuples in lable images instead of defining a empty list