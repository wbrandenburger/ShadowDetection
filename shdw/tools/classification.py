# ===========================================================================
#   classification.py -------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.data
import shdw.tools.imgtools

import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_mlp_classification(
    files, 
    specs,
    output,
    scale=100, 
    param_label=dict(), 
):
    shdw.__init__._logger.debug("Start creation of maximum likelihood classification with settings:\n'specs':\t'{}',\n'output':\t'{}',\n'scale':\t'{}'".format(specs, output, scale))

    img_set, save = shdw.tools.data.get_data(files, specs=specs, **output, scale=scale, param_label=param_label, show=False, live=True)

    for item in iter(img_set):
        print(item[0].path)
    #     item[0].path # save()