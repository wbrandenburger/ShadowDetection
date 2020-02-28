# ===========================================================================
#   classification.py -------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.data
import shdw.tools.imgtools
import shdw.tools.imagestats
import shdw.tools.welford

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
    shdw.__init__._logger.debug("Start creation of maximum likelihood classification map with settings:\n'specs':\t'{}',\n'output':\t'{}',\n'scale':\t'{}',\n'param_label':\t'{}'".format(specs, output, scale, param_label))

    img_set, save = shdw.tools.data.get_data(files, specs=specs, **output, scale=scale, param_label=param_label, show=False, live=True)

    stats = [shdw.tools.welford.Welford()]*len(param_label)

    for item in iter(img_set):
        label_masks = shdw.tools.imgtools.get_label_mask(item[specs.index("label")].data, param_label.values())
        for label in range(len(param_label.keys())):
            img = item[specs.index("msi")].data[label_masks[...,label],0]
            if len(img):
                stats[label].update(img[:])
        print(stats)
    
        #save(item[0].path, label_masks[...,[0,1,2]])
        # print(item[0].path)

        # imgstats = shdw.tools.imagestats.ImageStats(cat=param_label.values(), channels=8)
        # imgstats(item[specs.index("msi")].data, item[specs.index("label")].data) 
        # print(imgstats)
    #     item[0].path # save()