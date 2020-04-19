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
def new_distance_transform_map(
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

        edt = np.squeeze(
            shdw.utils.imgtools.get_distance_transform(
                item.spec("label").data,
                param["label_value"], 
                param["threshold"]
            ),
            axis=2
        )

        _logger.info(shdw.utils.imgtools.get_array_info(edt))
        
        img_out(item[0].path, edt)

        