# ===========================================================================
#   experiments.py ----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.tools.imgcontainer
import shdw.utils.general
import source.freitas.shdwDetection
import source.silva.Shadow_Detection

import cv2
import pathlib
import tifffile
import os

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def resize_img(img, scale):

    width = int(img.shape[1] * scale / 100.)
    height = int(img.shape[0] * scale / 100.)
    dim = (width, height) 

    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def read_image(path, scale):
    img = tifffile.imread(path)
    img = resize_img(img, scale)
    return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data(files, path_dir=os.environ.get("TEMP"), path_name="{}", regex=[".*",0], resize=100):

    load = lambda path, spec: read_image(path, resize)
    
    img_set = list()
    for f_set in files:
        img = shdw.tools.imgcontainer.ImgListContainer(load=load)
        for f in f_set:
            img.append(path = f, spec="image", live=True)
        img_set.append(img)

    get_path = shdw.utils.general.PathCreator(path_dir, path_name, *regex)
    save = lambda path, img: tifffile.imwrite(get_path(path), img)

    return img_set, save

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_freitas(files, output, resize=100):
    img_set, save = get_data(files, **output, resize=resize)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        save(item[0].path, img_shdw)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_silva(files, output, resize=100):
    img_set, save = get_data(files, **output, resize=resize)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.silva.Shadow_Detection.shadow_detection(
            item[0].path,
            convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
        )
        save(item[0].path, img_shdw[0,...]*255)
