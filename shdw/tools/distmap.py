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
def new_distance_transform_map(
    files,
    specs,
    output,
    param_label=dict(), 
    scale=100, 
    label_value=0, 
    threshold=10
):
    shdw.__init__._logger.debug("Start creation of distance transform maps (Bischke et. al.) with settings:\n'output':\t'{}',\n'scale':\t'{}',\n'label':\t'{}',\n'threshold':\t'{}'".format(output, scale, label_value, threshold))
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale, param_label=param_label, specs=specs, show=False, live=True)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path)) 

        edt = shdw.tools.imgtools.get_distance_transform(
            item.spec("label").data,
            label_value, threshold
        )

        save(item[0].path, edt)