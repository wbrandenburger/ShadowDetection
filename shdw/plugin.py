# ===========================================================================
#   plugin.py ---------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from shdw.__init__ import _logger 
import shdw.config.settings

import importlib
import pathlib
import re

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def stevedore_error_handler(manager, entrypoint, exception):
    _logger.error(
        "Error while loading entrypoint [{0}]".format(entrypoint)
    ) # @log
    _logger.error(exception) # @log

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_module(module):
    module = module if isinstance(module, list) else [module]

    module_name = "shdw"
    for sub_module in module:
        module_name = "{0}.{1}".format(module_name, sub_module)

    _logger.debug("Import module '{0}'".format(module_name))

    return (importlib.import_module(module_name), module_name)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_module_from_submodule(module, submodule):
    return get_module([module, submodule])

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_module_task(module, task, submodule=None):
    if submodule is not None:
        module = get_module_from_submodule(module, submodule)[0]

    return getattr(
        module,
        task
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_tasks():
    module = importlib.import_module("shdw.{0}".format(shdw.config.settings._TASK_DIR))

    path = pathlib.Path(module.__file__).parent
    file_list = [str(f.stem) for f in path.iterdir() if f.is_file() and re.compile("[^__.+__$]").match(str(f.stem))]

    if file_list == list():
        raise ValueError("The predefined task folder seems to be empty.")

    return file_list

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_module_functions(module):
    task_list = list()
    for task in dir(module):
        if re.compile(shdw.config.settings._TASK_PREFIX).match(task):
            task_list.append(task.replace(shdw.config.settings._TASK_PREFIX ,"",1))
    return task_list
