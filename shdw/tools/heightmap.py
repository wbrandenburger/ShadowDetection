# ===========================================================================
#   heightmap.py ------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from shdw.__init__ import _logger
import shdw.utils.ply
import shdw.config.settings
import shdw.utils.imgtools

import tempfile
import subprocess
import pandas
import pathlib

import cv2
import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_height_map(img, height=dict(), show=False):
    dim_new = (img.shape[0]*img.shape[1])
    img = shdw.utils.imgtools.expand_image_dim(img.astype(float))

    if show:
        height_factor = float(np.max(img))/(float(np.max([img.shape[0], img.shape[1]])) / 10)
        img = img/height_factor

    grid = np.indices((img.shape[0], img.shape[1]), dtype="float")
    height.update( 
        {
            'x': grid[0,...].reshape(dim_new).T, 
            'y': grid[1,...].reshape(dim_new).T, 
            'z': img[...,0].reshape(dim_new).T
        }
    )
    return height

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def colorize_height_map(img, height=dict()):
    img_width, img_height, _ = img.shape
    dim_new =(img_width*img_height)

    height.update(
        {
            'red': img[:,:,0].reshape((img.shape[0]*img.shape[1])).T, 
            'green': img[:,:,1].reshape((img.shape[0]*img.shape[1])).T, 
            'blue': img[:,:,2].reshape((img.shape[0]*img.shape[1])).T
        }
    )
    return height

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def add_intensity_to_height_map(img, height=dict()):
    try:
        img_width, img_height, _ = img.shape
        dim_new =(img_width*img_height)

        height.update(
            {
                'intensity': img[:,:,1].reshape((img.shape[0]*img.shape[1])).T
            }
        )
    except AttributeError:
        pass
    return height

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_colorized_height_map(img, height, label=None, show=False):
    data = get_height_map(height, show=show)
    data = colorize_height_map(img, data)
    try:
        data = add_intensity_to_height_map(label, data)
    except ValueError:
        pass
    return data

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def write_height_map(img, height, path):
    data = pandas.DataFrame(height, index=range(img.shape[0]*img.shape[1]))

    # write to temporary file
    _logger.info("[SAVE] '{}'".format(path))
    shdw.utils.ply.write_ply(path, points=data)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def read_height_map(path):
    return shdw.utils.ply.read_ply(path)["points"]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_normal_image(img, height, bins=None, verbose=False, show=False):
    data = get_colorized_height_map(img, height, show=show)

    # create a temporary file
    path = tempfile.mkstemp(prefix="shdw-", suffix=".ply")[1]
    write_height_map(img, data, path)

    compute_normals(path, verbose=verbose)

    normals = read_height_map(path)["nz"].to_numpy().reshape(height.shape)*(-1.)+1. 
    normals = np.where(normals>0., normals, np.min(normals[normals>0.]))
    normals = shdw.utils.imgtools.project_data_to_img(-np.log(normals))

    if bins:
        normals = np.ceil(normals*bins)
        normals = (np.where(normals==0., 1., normals) - 1.)/(bins-1.)

    return normals

    # plt.hist(hm.reshape(-1,1),bins="auto", histtype="step")
    # print(np.unique(hm))
    # plt.show()
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def compute_normals(path, verbose=False):
    args = shdw.config.settings._SETTINGS["cloud_normals_args"]

    cloud_process = "cloud_process" if not verbose else "cloud_process_verbose"
    process = subprocess.Popen(
        get_args(
            shdw.config.settings._SETTINGS[cloud_process], 
            [item.format(**{"obj": { "path": path}}) for item in args]
        )
    )
    process.wait()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def compute_mesh(path, verbose=False):
    args = shdw.config.settings._SETTINGS["cloud_delaunay_args"]

    cloud_process = "cloud_process" if not verbose else "cloud_process_verbose"
    process = subprocess.Popen(
        get_args(
            shdw.config.settings._SETTINGS[cloud_process], 
            [item.format(**{"obj": { "path": path}}) for item in args]
        )
    )
    process.wait()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def open_height_map(path, ccviewer=False):
    if ccviewer:
        subprocess.Popen(
            get_args( shdw.config.settings._SETTINGS["cloud_viewer"], path)
        )
    else:          
        subprocess.Popen( 
            get_args(shdw.config.settings._SETTINGS["cloud_editor"],path)
        )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def main(img, height, label=None, verbose=False, normals=False, mesh=False, ccviewer=True, attempt=False, show=False):

    data = get_colorized_height_map(img, height, label=label, show=show)

    # create a temporary file
    path = tempfile.mkstemp(prefix="shdw-", suffix=".ply")[1]
    write_height_map(img, data, path)

    if normals:
        compute_normals(path, verbose=verbose)
    if mesh:
        compute_mesh(path, verbose=verbose)

    open_height_map(path, ccviewer=ccviewer)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------   
def get_args(cmd, *args):
    cmd = cmd.copy() if isinstance(cmd, list) else [cmd]
    for a in args:
        cmd.extend(*to_list(a))
    
    return " ".join(cmd)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def to_list(*args):
    return (x if isinstance(x, list) or x is None else [x] for x in args)
