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
def new_tiles(
    files,
    param_specs,
    param_io,
    param_show=dict(),
    param=dict(),
):
    _logger.debug("Start creation of normal maps with settings:\nparam_specs:\t{},\nparam_io:\t{},\nparam_show:\t{},\nparam:\t{}".format(param_specs, param_io, param_show, param))

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------
    img_in, img_out, _, _ = shdw.utils.imgio.get_data(files, param_specs, param_io, param_show=param_show)

    for item_list in img_in:
        for index, item in enumerate(item_list):
            _logger.debug("Processing image '{}'".format(item.path)) 
        
            img = shdw.utils.imgtools.expand_image_dim(item.data)
            try:
                tiles = param["tiles"]
            except KeyError:
                tiles = img.shape

            img_out(item.path, img[0:tiles[0], 0:tiles[1], :], index=index)