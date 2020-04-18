# ===========================================================================
#   shadows.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from shdw.__init__ import _logger
import shdw.utils.imgio
import source.freitas.shdwDetection
import source.silva.Shadow_Detection

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_shadow_map_freitas(
    files, 
    param_specs,
    param_io,
    param_show=dict(),
):
    _logger.debug("Start creation of shadow maps (Freitas et. al.)  with settings:\nparam_specs:\t{},\nparam_io:\t{},\nparam_label:\t{},\nparam_show:\t{},\nparam:\t{}".format(param_specs, param_io, param_show))

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------
    img_in, img_out, _, _ = shdw.utils.imgio.get_data(files, param_specs, param_io, param_show=param_show)

    for item in img_in:
        _logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.freitas.shdwDetection.shadowDetection_Santos_KH(item[0].data)

        img_out(item[0].path, img_shdw)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_shadow_map_silva(
    files, 
    param_specs,
    param_io,
    param_show=dict(),
):
    _logger.debug("Start creation of shadow maps (Silva et. al.)  with settings:\nparam_specs:\t{},\nparam_io:\t{},\nparam_label:\t{},\nparam_show:\t{},\nparam:\t{}".format(param_specs, param_io, param_show))

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------
    img_in, img_out, _, _ = shdw.utils.imgio.get_data(files, param_specs, param_io, param_show=param_show)

    for item in img_in:
        _logger.debug("Processing image '{}'".format(item[0].path))
        img_shdw = source.silva.Shadow_Detection.shadow_detection(
            item[0].path,
            convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
        )
        img_out(item[0].path, img_shdw[0,...]*255)
