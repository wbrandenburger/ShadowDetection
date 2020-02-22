# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.tools.imgio
import shdw.tools.imgcontainer

import os

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data(files, path_dir=os.environ.get("TEMP"), path_name="{}", regex=[".*", 0], scale=100):

    load = lambda path, spec: shdw.tools.imgio.get_image(path, scale=scale)
    
    img_set = list()
    for f_set in files:
        img = shdw.tools.imgcontainer.ImgListContainer(load=load)
        for f in f_set:
            img.append(path = f, spec="image", live=True)
        img_set.append(img)

    get_path = shdw.utils.general.PathCreator(path_dir, path_name, *regex)
    save = lambda path, img: shdw.tools.imgio.save_image(get_path(path), img)

    return img_set, save

