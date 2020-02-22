# ===========================================================================
#   imagetools.py -----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import cv2
import numpy as np
from matplotlib import pyplot as plt

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def expand_image_dim(img):
    return np.expand_dims(img, axis=2) if len(img.shape) != 3 else img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def stack_image_dim(img):
    return np.stack([img]*3, axis=2) if len(img.shape) != 3 else img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def resize_img(img, scale):

    width = int(img.shape[1] * scale / 100.)
    height = int(img.shape[0] * scale / 100.)
    dim = (width, height) 

    img = cv2.resize(img, dim,  interpolation=cv2.INTER_NEAREST)
    return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def project_data_to_img(img):
    img = img.astype(float)
    min_max_img = (np.min(img), np.max(img))
    # img[~np.isnan(img)]
    img = (img - min_max_img[0])/(min_max_img[1] - min_max_img[0]) * 255
    img = img.astype("uint8")
    return img

def project_dict_to_img(obj):
    img = np.fromiter(obj.values(), dtype=np.uint8)
    return project_data_to_img(img)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def raise_contrast(img):
    for c in range(0, img.shape[2]):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img[:,:,c] = clahe.apply(img[:,:,c])

    return img

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def labels_to_image(img, labels):
    img = expand_image_dim(img).astype(int)
    dim = img.shape
    label = np.zeros((img.shape[0], img.shape[1]), dtype=int)
    for c in range(img.shape[-1]):
        label += img[:, :, c]*int(pow(2, c))
    
    lut = lambda x: labels[str(x)]
    np_lut = np.vectorize(lut, otypes=[np.uint8])
    label = np_lut(label.astype(int))
    return label

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_label_image(img, label, value, equal=True):
    img_label = img.copy()
    for c in range(img.shape[-1]):
        if equal:
            mask = np.ma.masked_where(label[...,-1] != value, img[...,c])
        else:
            mask = np.ma.masked_where(label[...,-1] == value, img[...,c])
                    
        np.ma.set_fill_value(mask, 0)
        img_label[:,:,c] = mask.filled()
    return img_label