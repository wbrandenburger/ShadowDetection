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
def new_gaussian_map(
    files,
    specs,
    output,
    param_label=dict(), 
    scale=100, 
    stats=[0.0, 0.2]
):
    shdw.__init__._logger.debug("Start creation of gaussian maps with settings:\noutput:\t{}\nscale:\t{}\nstats:\t{}".format(output, scale, stats))
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale, specs=specs)    
    
    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))

        img = item[0].data
        shdw.__init__._logger.debug("Result with {}".format(shdw.tools.imgtools.get_img_information(img)))
        gaussian_map = shdw.tools.imgtools.gaussian_kernel(img.shape[0], img.shape[1], mu=stats[0], sigma=stats[1])
        save(item[0].path, gaussian_map)
