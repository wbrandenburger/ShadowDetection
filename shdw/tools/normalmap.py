# ===========================================================================
#   distmap.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.data
import shdw.tools.heightmap

import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_normal_map(
    files,
    specs,
    output,
    scale=100,
    bins=None,
    show=False
):
    shdw.__init__._logger.debug("Start creation of normal maps with settings:\n'output':\t'{}',\n'scale':\t'{}',\n".format(output, scale))
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale, specs=specs, show=False, live=True)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path)) 

        nm = shdw.tools.heightmap.get_normal_image(item.spec("image").data,item.spec("height").data, bins=bins)
        save(item[0].path, nm)