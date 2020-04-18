# ===========================================================================
#   distmap.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from shdw.__init__ import _logger
import shdw.tools.heightmap
import shdw.utils.imgio
import shdw.utils.imgtools

import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_normal_map(
    files, 
    param_specs,
    param_io,
    param_show=dict(),
    param=dict()
):
    _logger.debug("Start creation of maximum likelihood classification map with settings:\nparam_specs:\t{},\nparam_io:\t{},\nparam_show:\t{},\nparam:\t{}".format(param_specs, param_io, param_show, param))

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------
    img_in, img_out, _, _ = shdw.utils.imgio.get_data(files, param_specs, param_io, param_show=param_show)

    for item in img_in:
        _logger.debug("Processing image '{}'".format(item[0].path)) 

        nm = shdw.tools.heightmap.get_normal_image(item.spec("image").data,item.spec("height").data, bins=param["bins"])
        img_out(item[0].path, nm)