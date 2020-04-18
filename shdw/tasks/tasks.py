# ===========================================================================
#   tasks.py ----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from shdw.__init__ import _logger
import shdw.config.settings
import shdw.utils.format
import shdw.utils.general as glu

import shdw.tools.classification
import shdw.tools.distmap
import shdw.tools.gaussianmap
import shdw.tools.normalmap
import shdw.tools.shadows
import shdw.tools.tiles

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_default():
    """Default task of set 'test'"""
    _logger.warning("No task chosen from set 'tests'")

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_mlp(setting="training"):
    stats = shdw.tools.classification.new_mlp_classification_stats(
        shdw.config.settings.get_data(setting="training"),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_label"],
        shdw.config.settings._SETTINGS["param"]
    )

    shdw.tools.classification.new_mlp_classification_map(
        stats,
        shdw.config.settings.get_data(setting="test"),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_label"],
        shdw.config.settings._SETTINGS["param_class"],
        shdw.config.settings._SETTINGS["param"]
    )

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_mlp_mv():
    stats = shdw.tools.classification.new_mlp_classification_stats(
        shdw.config.settings.get_data(setting="training"),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_label"],
        shdw.config.settings._SETTINGS["param"]
    )

    shdw.tools.classification.new_mlp_mv_classification_map(
        stats,
        shdw.config.settings.get_data(setting="test"),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_label"],
        shdw.config.settings._SETTINGS["param_class"],
        shdw.config.settings._SETTINGS["param"]
    )

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_distance_transform_map(setting="training"):
    shdw.tools.distmap.new_distance_transform_map(
        shdw.config.settings.get_data(setting),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_label"],
        shdw.config.settings._SETTINGS["param_show"],        
        shdw.config.settings._SETTINGS["param"]
    )

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_normal_map(setting="training"):
    shdw.tools.normalmap.new_normal_map(
        shdw.config.settings.get_data(setting),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_show"],
        shdw.config.settings._SETTINGS["param"]
    )

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_gaussian_map(setting="training"):
    shdw.tools.gaussianmap.new_gaussian_map(
        shdw.config.settings.get_data(setting),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_label"],
        shdw.config.settings._SETTINGS["param_show"],        
        shdw.config.settings._SETTINGS["param"]
    )

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_tiles(setting="training"):
    shdw.tools.tiles.new_tiles(
        shdw.config.settings.get_data(setting),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param"]
    )


#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_shadow_map_freitas(setting="training"):
    shdw.tools.shadows.new_shadow_map_freitas(
        shdw.config.settings.get_data(setting),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_show"]
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_shadow_map_silva(setting="training"):
    shdw.tools.shadows.new_shadow_map_silva(
        shdw.config.settings.get_data(setting),
        shdw.config.settings._SETTINGS["param_specs"],
        shdw.config.settings._SETTINGS["param_io"],
        shdw.config.settings._SETTINGS["param_show"]
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_print_user_settings():
    """Print the user settings"""
    
    # print user's defined settings
    _logger.info("Print user's defined settings")
    shdw.utils.format.print_data(shdw.config.settings._SETTINGS)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_print_user_data():
    """Print the user data"""
    
    # print user's defined data
    _logger.info("Print user's defined data")
    shdw.utils.format.print_data(shdw.config.settings.get_data_dict())