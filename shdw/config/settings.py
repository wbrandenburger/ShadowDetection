# ===========================================================================
#   settings.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import rsvis.__init__
import rsvis.utils.yaml

import os

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_SETTINGS = dict()
_DATA = list() 

_TASK_DIR = "tasks"
_DEFAULT_TASK = "default"

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_settings(path):
    """Read general settings file and assign content to global settings object.

    If general settings file does not exist an error is raised.

    :param path: Path of genereal settings file
    :type path: str
    """
    global _SETTINGS
    
    # if general settings file does not exist raise error
    if not os.path.isfile(path):
        raise IOError("Settings file {0} with experiment settings does not exist".format(settings_file))
    
    # read general settings file and assign content to global settings object
    rsvis.__init__._logger.debug("Read settings file {0}:".format(path))
    _SETTINGS = rsvis.utils.yaml.yaml_to_data(path, raise_exception=True)
    
    get_data()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data(setting = "training"):
    global _DATA
    if setting in _SETTINGS.keys():
        with open(_SETTINGS[setting]) as f:
            _DATA = [line.split() for line in f]