# ===========================================================================
#   experiments.py ----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.tools.imgcontainer
import shdw.utils.regex
import source.freitas.shdwDetection

import pathlib
import tifffile

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def read_image(path):
    return tifffile.imread(path)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def save_image(path, img, dest_dir, dest_basename, research):
    dest_path = pathlib.Path(dest_dir) / dest_basename.format(research(pathlib.Path(path).stem))
    shdw.__init__._logger.debug("Save image to location '{}'".format(dest_path))
    tifffile.imwrite(dest_path, img)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_freitas(files, dest_dir, dest_basename, io):

    load = lambda path, spec: read_image(path)
    
    img_set = list()
    for f_set in files:
        img = shdw.tools.imgcontainer.ImgListContainer(load=load)
        for f in f_set:
            img.append(path = f, spec="image", live=True)
        img_set.append(img)

    research = shdw.utils.regex.ReSearch(*io)
    save = lambda path, img: save_image(path, img, dest_dir, dest_basename, research)
    
    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        save(item[0].path, img_shdw)

    # # import shadow.rsddec.Shadow_Detection
    # # a = shadow.rsddec.Shadow_Detection.shadow_detection(
    # #     img_set[0][0].path,
    # #     ".\shadow-mask.tif", 
    # #     convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
    # # )
    # # print(a)
    # # import tifffile
    # # tifffile.imwrite(".\shadow.tif",a*255)

