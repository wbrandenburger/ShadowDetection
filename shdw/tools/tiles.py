# ===========================================================================
#   distmap.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.data
import shdw.tools.imgtools

import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_tiles(
    files,
    specs,
    output,
    param=dict(),
    tiles=None
):
    shdw.__init__._logger.debug("Start creation of normal maps with settings:\n'output':\t'{}',\n'param':\t'{}',\n".format(output, param))
    img_set, save = shdw.tools.data.get_data(files, **output, specs=specs)

    for item_list in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item_list[0].path)) 
        for index, item in enumerate(item_list):
            shdw.__init__._logger.debug("Processing image '{}'".format(item.path)) 
        
            img = shdw.tools.imgtools.expand_image_dim(item.data)
            if not tiles:
                tiles = img.shape

            save(item.path, img[0:tiles[0], 0:tiles[1], :], index=index)