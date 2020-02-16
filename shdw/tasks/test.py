# ===========================================================================
#   test.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import rsvis.__init__
import rsvis.config.settings
import rsvis.utils.format
import rsvis.tools.rsshow
import rsvis.tools.lecture

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def main():
    
    test_user_data()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_image(path, spec, labels=dict(), scale=100):
    import tifffile
    import rsvis.tools.imgtools
    img = tifffile.imread(path)
    img = rsvis.tools.imgtools.resize_img(img, scale)

    if spec == "label":
        img = rsvis.tools.imgtools.labels_to_image(img, labels)
        
    if spec in ["label", "height", "msi"]:
        img = rsvis.tools.imgtools.project_data_to_img(img)

    img =  rsvis.tools.imgtools.stack_image_dim(img)

    return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_shadow():
    import rsvis.config.settings
    files = *rsvis.config.settings._DATA, 
    specs = rsvis.config.settings._SETTINGS["data-tensor-types"], 
    labels = rsvis.config.settings._SETTINGS["label"],
    resize = rsvis.config.settings._SETTINGS["resize"]

    load = lambda path, spec: get_image(path, spec, labels=labels, scale=resize)

    import rsvis.tools.imgcontainer
    img_set = list()
    for f_set in files:
        img = rsvis.tools.imgcontainer.ImgListContainer(load=load)
        for f, s  in zip(f_set, specs):
            # live = False if s == "label" else True
            img.append(path = f, spec=s)
        img_set.append(img)
    
    import tifffile
    # import shadow.rsddec.Shadow_Detection
    # a = shadow.rsddec.Shadow_Detection.shadow_detection(
    #     img_set[0][0].path,
    #     ".\shadow-mask.tif", 
    #     convolve_window_size = 5, num_thresholds = 3, struc_elem_size = 5
    # )
    # print(a)
    # import tifffile
    # tifffile.imwrite(".\shadow.tif",a*255)
    import shadow.outsddec.shdwDetection

    imgRef = img_set[0][0].data
    imgOut = shadow.outsddec.shdwDetection.shadowDetection_Santos_KH(imgRef)
    print(imgOut)
    tifffile.imwrite(".\shadow.tif", imgOut)



#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_rsshow():
    rsvis.tools.rsshow.rsshow(
        rsvis.config.settings._DATA, 
        rsvis.config.settings._SETTINGS["data-tensor-types"], 
        labels=rsvis.config.settings._SETTINGS["label"],
        resize=rsvis.config.settings._SETTINGS["resize"]
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_code():
    rsvis.tools.rsshow.test_code( rsvis.config.settings._DATA, 
        rsvis.config.settings._SETTINGS["data-tensor-types"])

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_lecture():
    rsvis.tools.lecture.test(
        rsvis.config.settings._DATA, 
        rsvis.config.settings._SETTINGS["data-tensor-types"], 
        cat=rsvis.config.settings._SETTINGS["label"],
        resize=rsvis.config.settings._SETTINGS["resize"]
    )
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_user_settings():
    """Print the user settings"""
    
    # print user's defined settings
    rsvis.__init__._logger.info("Print user's defined settings")
    rsvis.utils.format.print_data(rsvis.config.settings._SETTINGS)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_user_data():
    """Print the user data"""
    
    # print user's defined data
    rsvis.__init__._logger.info("Print user's defined data")
    rsvis.utils.format.print_data(rsvis.config.settings._DATA)