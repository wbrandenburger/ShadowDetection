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
def new_shadow_map_freitas(
    files, 
    specs,
    output, 
    scale=100
):
    shdw.__init__._logger.debug("Start creation of shadow maps (Freitas et. al.) with settings:\n'output':\t'{}',\n'scale':\t{}".format(output, scale))
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        save(item[0].path, img_shdw)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_shadow_map_silva(
    files,
    specs,
    output, 
    scale=100
):
    shdw.__init__._logger.debug("Start creation of shadow maps (Silva et. al.) with settings:\n'output':\t'{}',\n'scale':\t{}".format(output, scale))
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.silva.Shadow_Detection.shadow_detection(
            item[0].path,
            convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
        )
        save(item[0].path, img_shdw[0,...]*255)
