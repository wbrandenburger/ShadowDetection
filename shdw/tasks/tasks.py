# ===========================================================================
#   tasks.py ----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.config.settings
import shdw.utils.format

import shdw.tools.distmap
import shdw.tools.shadows
import shdw.tools.classification

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_default():
    task_print_user_settings()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
get_value = lambda obj, key, default: obj[key] if key in obj.keys() else default

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_mlp():
    try:
        stats = shdw.tools.classification.new_mlp_classification_stats(
            shdw.config.settings.get_data(setting="training"),
            shdw.config.settings._SETTINGS["data-tensor-types"],
            shdw.config.settings._SETTINGS["output"],
            param_label=shdw.config.settings._SETTINGS["param_label"],
            param=shdw.config.settings._SETTINGS["param"]
        )

        shdw.tools.classification.new_mlp_classification_map(
            stats,
            shdw.config.settings.get_data(setting="test"),
            shdw.config.settings._SETTINGS["data-tensor-types"],
            shdw.config.settings._SETTINGS["output"],
            param_label=shdw.config.settings._SETTINGS["param_label"],
            param_specs=shdw.config.settings._SETTINGS["param_specs"],
            param=shdw.config.settings._SETTINGS["param"],
            log=shdw.config.settings._SETTINGS["log"]
        )
    except KeyError:
        return

# function ------------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_distance_transform_map(setting="training"):
    try:
        shdw.tools.distmap.new_distance_transform_map(
            shdw.config.settings.get_data(setting),
            shdw.config.settings._SETTINGS["data-tensor-types"],
            shdw.config.settings._SETTINGS["output"],
            param_label = shdw.config.settings._SETTINGS["param_label"],
            **shdw.config.settings._SETTINGS["param"]
        )
    except KeyError:
        pass

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_shadow_map_freitas(setting="training"):
    try:
        shdw.tools.shadows.new_shadow_map_freitas(
            shdw.config.settings.get_data(setting),
            shdw.config.settings._SETTINGS["data-tensor-types"],
            shdw.config.settings._SETTINGS["output"],
            scale=get_value(shdw.config.settings._SETTINGS,"scale", 100)
        )
    except KeyError:
        pass

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_new_shadow_map_silva(setting="training"):
    try:
        shdw.tools.shadows.new_shadow_map_silva(
            shdw.config.settings.get_data(setting),
            shdw.config.settings._SETTINGS["output"],
            scale=get_value(shdw.config.settings._SETTINGS,"scale", 100)
        )
    except KeyError:
        pass

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_print_user_settings():
    """Print the user settings"""
    
    # print user's defined settings
    shdw.__init__._logger.info("Print user's defined settings")
    shdw.utils.format.print_data(shdw.config.settings._SETTINGS)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_print_user_data():
    """Print the user data"""
    
    # print user's defined data
    shdw.__init__._logger.info("Print user's defined data")
    shdw.utils.format.print_data(shdw.config.settings.get_data_dict())