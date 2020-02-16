# ===========================================================================
#   plugin.py ---------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import rsvis.__init__
import rsvis.config.settings

import importlib
import logging
import os
import re

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def stevedore_error_handler(manager, entrypoint, exception):
    rsvis.__init__._logger.error(
        "Error while loading entrypoint [{0}]".format(entrypoint)
    ) # @log
    rsvis.__init__._logger.error(exception) # @log

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_tasks():
    module = importlib.import_module("rsvis.{0}".format(rsvis.config.settings._TASK_DIR))
    path = os.path.dirname(module.__file__)
    file_list = [os.path.splitext(f)[0] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and re.compile("[^__.+__$]").match(f)]

    if file_list == list():
        raise ValueError("The predefined task folder seems to be empty.")

    return file_list

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_task_module(task):
    module_name = "rsvis.{0}.{1}".format(rsvis.config.settings._TASK_DIR, task)
    rsvis.__init__._logger.debug("Import task module '{0}'".format(module_name))
    
    return (importlib.import_module(module_name), module_name)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_module_functions(module, regex):
    return [ f for f in dir(module) if re.compile(regex).match(f) ] 

