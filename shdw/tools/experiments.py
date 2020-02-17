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

import pathlib
import tifffile

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def read_image(path):
    return tifffile.imread(path)

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class PathCreator():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, dest_dir, dest_basename, regex=".*", group=0):
        self._dest_dir = pathlib.Path(dest_dir)
        self._dest_basename = dest_basename
        self._research = shdw.utils.regex.ReSearch(regex, group)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __call__(self, path):
        return self._dest_dir / self._dest_basename.format(self._research(pathlib.Path(path).stem))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data(files, dest_dir, dest_basename, io):

    load = lambda path, spec: read_image(path)
    
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
def get_shadow_freitas(files, dest_dir, dest_basename, io):
    img_set, save = get_data(files, dest_dir, dest_basename, io)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        save(item[0].path, img_shdw)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_silva(files, dest_dir, dest_basename, io):
    img_set, save = get_data(files, dest_dir, dest_basename, io)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.silva.Shadow_Detection.shadow_detection(
            item[0].path,
            convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
        )
        save(item[0].path, img_shdw[0,...]*255)
