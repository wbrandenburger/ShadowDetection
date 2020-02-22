# ===========================================================================
#   distmask.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.data

import numpy as np
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_distance_mask(files, output, scale=100, labels=dict()):
    img_set, save = shdw.tools.data.get_data(files, **output, scale=scale, labels=labels, default_spec="label", show=True, live=True)

    for item in iter(img_set):
        shdw.__init__._logger.debug("Processing image '{}'".format(item[0].path))        
        #print(np.unique(item[0].data))

        # rsvis.tools.imgtools.get_label_image(
        #         obj.get_img(), 
        #         obj.get_img_from_spec("label"), 
        #         value=label_index(),
        #         equal=True),                 
        #     show=True
        # )
        save(item[0].path, item[0].data)