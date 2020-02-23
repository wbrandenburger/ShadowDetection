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
def new_distance_transfrom_map(
    files, 
    output,
    labels=dict(), 
    scale=100, 
    label= 0, 
    threshold=10
):
    shdw.__init__._logger.debug("Start creation of distance transform maps (Bischke et. al.) with settings:\n'output':\t'{}',\n'scale':\t'{}',\n'label':\t'{}',\n'threshold':\t'{}'".format(output, scale, label, threshold))
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale, labels=labels, default_spec="label", show=False, live=True)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path)) 

        edt = shdw.tools.imgtools.get_distance_transform(item[0].data, label, threshold)
        save(item[0].path, edt)