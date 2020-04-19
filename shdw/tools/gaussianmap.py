# ===========================================================================
#   distmap.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from shdw.__init__ import _logger
import shdw.utils.imgio
import shdw.utils.imgtools

import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_gaussian_map(
    files, 
    param_specs,
    param_io,
    param_label=dict(),
    param_show=dict(),
    param=dict()
):
    _logger.info("Start creation of maximum likelihood classification map with settings:\nparam_specs:\t{},\nparam_io:\t{},\nparam_label:\t{},\nparam_show:\t{},\nparam:\t{}".format(param_specs, param_io, param_label, param_show, param))

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------  
    img_in, img_out, _, _ = shdw.utils.imgio.get_data(files, param_specs, param_io, param_label=param_label, param_show=param_show)

    for item in img_in:
        _logger.info("Processing image '{}'".format(item[0].path))

        img = item[0].data
        _logger.info("Result with {}".format(shdw.utils.imgtools.get_array_info(img)))
        gaussian_map = shdw.utils.imgtools.gaussian_kernel(img.shape[0], img.shape[1], mu=param["stats"][0], sigma=param["stats"][1])
        img_out(item[0].path, gaussian_map)
