# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.utils.general
import shdw.tools.imgio
import shdw.tools.imgcontainer

import os

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data(files, path_dir=os.environ.get("TEMP"), path_name="{}", regex=[".*", 0], scale=100, param_label=dict(), default_spec="image", show=False, live=True, specs=list()):

    load = lambda path, spec: shdw.tools.imgio.get_image(path, spec=spec, param_label=param_label, scale=scale, show=show)
    
    img_set = list() 
    for f_set in files:
        img = shdw.tools.imgcontainer.ImgListContainer(load=load)
        if not specs:
            for f in f_set:
                img.append(path = f, spec=default_spec, live=live)
        else:
            for f, s in zip(f_set, specs):
                img.append(path = f, spec=s, live=live)
        img_set.append(img)

    get_path = shdw.utils.general.PathCreator(path_dir, path_name, *regex)
    save = lambda path, img: shdw.tools.imgio.save_image(get_path(path), img)

    return img_set, save

