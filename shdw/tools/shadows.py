# ===========================================================================
#   shadows.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.tools.data
import source.freitas.shdwDetection
import source.silva.Shadow_Detection

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_freitas(files, output, scale=100):
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        save(item[0].path, img_shdw)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_shadow_silva(files, output, scale=100):
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.silva.Shadow_Detection.shadow_detection(
            item[0].path,
            convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
        )
        save(item[0].path, img_shdw[0,...]*255)
