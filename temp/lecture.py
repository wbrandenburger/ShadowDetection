# ===========================================================================
#   lecture.py --------------------------------------------------------------
# ===========================================================================

import rsvis.tools.rsshow
import rsvis.tools.imagestats
import cv2
import numpy as np
import rsvis.tools.welford
import timeit
import tifffile
import matplotlib.pyplot as plt

# #   function ----------------------------------------------------------------
# # ---------------------------------------------------------------------------
# def task_test_lecture():
#     rsvis.tools.lecture.test(
#         rsvis.config.settings._DATA, 
#         rsvis.config.settings._SETTINGS["data-tensor-types"], 
#         cat=rsvis.config.settings._SETTINGS["label"],
#         scale=get_value(rsvis.config.settings._SETTINGS,"scale", 100)
#     )

# #   function ----------------------------------------------------------------
# # ---------------------------------------------------------------------------
# def blubb(img, **kwargs): 
#     import rsvis.tools.imagestats   
#     foo = rsvis.tools.imagestats.ImageStats(
#             path="A:\\VirtualEnv\\dev-rsvis\\src\\rsvis\\tmpchlgw4dk.json" 
#         )
#     dim = img.shape
#     img = img.reshape(-1, dim[-1])
#     img = np.apply_along_axis(foo.get_probability_c, -1, img)
#     img = img.reshape( dim[0], dim[1], 1)
#     return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test(files, types, cat=dict(), scale=100):
    
    

    # foo = rsvis.tools.imagestats.ImageStats(cat.values(), 8 ) 
    for i in range(2,3):
        img_list = img_load(i)
    #     foo(img_list[types.index("msi")], img_list[types.index("label")]) 
    #     print(foo)

    # path = foo.write()
    # print(path)

    foo = rsvis.tools.imagestats.ImageStats(
            path="A:\\VirtualEnv\\dev-rsvis\\src\\rsvis\\temp\\tmpchlgw4dk.json" 
        )
    # foo.plot_stats(2)
    img = img_list[types.index("msi")]
    a = foo.get_probability(img[50,30,:])
    print(a)
    
def get_image(img_path, img_type, cat, scale=100):
    
    img = tifffile.imread(img_path)

    scale_percent = scale
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height) 
    img = cv2.resize(img, dim,  interpolation=cv2.INTER_NEAREST)

    img = np.expand_dims(img, axis=2) if len(img.shape) != 3 else img 

    if img_type == "label":
        img = rsvis.tools.rsshow.label_to_scalar(img, cat)
    if img_type == "msi":
        img = img.astype(float)
        min_max_img = (np.min(img), np.max(img))
        img = (img - min_max_img[0])/(min_max_img[1] - min_max_img[0]) * 255
        img = img.astype("uint8")

    return img