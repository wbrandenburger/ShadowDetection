# ===========================================================================
#   test.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.config.settings
import shdw.utils.format

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def main():
    
    test_user_data()

# #   function ----------------------------------------------------------------
# # ---------------------------------------------------------------------------
# def get_image(path, spec, labels=dict(), scale=100):
#     import tifffile
#     import shdw.tools.imgtools
#     img = tifffile.imread(path)
#     img = shdw.tools.imgtools.resize_img(img, scale)

#     if spec == "label":
#         img = shdw.tools.imgtools.labels_to_image(img, labels)
        
#     if spec in ["label", "height", "msi"]:
#         img = shdw.tools.imgtools.project_data_to_img(img)

#     img =  shdw.tools.imgtools.stack_image_dim(img)

#     return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
# def test_shadow():
#     import shdw.config.settings
#     files = *shdw.config.settings._DATA, 
#     specs = shdw.config.settings._SETTINGS["data-tensor-types"], 
#     labels = shdw.config.settings._SETTINGS["label"],
#     resize = shdw.config.settings._SETTINGS["resize"]

#     load = lambda path, spec: get_image(path, spec, labels=labels, scale=resize)

#     import shdw.tools.imgcontainer
#     img_set = list()
#     for f_set in files:
#         img = shdw.tools.imgcontainer.ImgListContainer(load=load)
#         for f, s  in zip(f_set, specs):
#             # live = False if s == "label" else True
#             img.append(path = f, spec=s)
#         img_set.append(img)
    
#     import tifffile

    # # import shadow.rsddec.Shadow_Detection
    # # a = shadow.rsddec.Shadow_Detection.shadow_detection(
    # #     img_set[0][0].path,
    # #     ".\shadow-mask.tif", 
    # #     convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
    # # )
    # # print(a)
    # # import tifffile
    # # tifffile.imwrite(".\shadow.tif",a*255)

    # import shadow.outsddec.shdwDetection

    # imgRef = img_set[0][0].data
    # imgOut = shadow.outsddec.shdwDetection.shadowDetection_Santos_KH(imgRef)
    # print(imgOut)
    # tifffile.imwrite(".\shadow.tif", imgOut)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_user_settings():
    """Print the user settings"""
    
    # print user's defined settings
    shdw.__init__._logger.info("Print user's defined settings")
    shdw.utils.format.print_data(shdw.config.settings._SETTINGS)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_user_data():
    """Print the user data"""
    
    # print user's defined data
    shdw.__init__._logger.info("Print user's defined data")
    shdw.utils.format.print_data(shdw.config.settings._DATA)