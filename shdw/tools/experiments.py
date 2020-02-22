# ===========================================================================
#   experiments.py ----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.tools.imgcontainer
import shdw.utils.regex
import source.freitas.shdwDetection
import source.silva.Shadow_Detection

import cv2
import pathlib
import tifffile

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
#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class PathCreator():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, dest_dir, dest_basename, regex=".*", group=0):
        self._dest_dir = pathlib.Path(dest_dir)
        self._dest_basename = dest_basename
        self._re_search = shdw.utils.regex.ReSearch(regex, group)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __call__(self, path):
        return self._dest_dir / self._dest_basename.format(self._re_search(pathlib.Path(path).stem))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data(files, dest_dir, dest_basename, io, resize=100):

    load = lambda path, spec: read_image(path, resize)
    
    img_set = list()
    for f_set in files:
        img = shdw.tools.imgcontainer.ImgListContainer(load=load)
        for f in f_set:
            img.append(path = f, spec="image", live=True)
        img_set.append(img)

    get_path = PathCreator(dest_dir, dest_basename, *io)
    save = lambda path, img: tifffile.imwrite(get_path(path), img)

    return img_set, save

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_freitas(files, dest_dir, dest_basename, io, resize=100):
    img_set, save = get_data(files, dest_dir, dest_basename, io, resize=resize)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        save(item[0].path, img_shdw)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_silva(files, dest_dir, dest_basename, io, resize=100):
    img_set, save = get_data(files, dest_dir, dest_basename, io, resize=resize)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.silva.Shadow_Detection.shadow_detection(
            item[0].path,
            convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
        )
        save(item[0].path, img_shdw[0,...]*255)
