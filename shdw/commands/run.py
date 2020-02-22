# ===========================================================================
#   run.py ------------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.config.settings
import shdw.plugin
import shdw.debug.exceptions

import click
import logging
import os
import sys

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
@click.command(
    "run",
    help="Blubb",
    context_settings=dict(ignore_unknown_options=True)
)
@click.help_option(
    "-h",
    "--help" 
)
@click.argument(
    "file", 
    type=str, 
    nargs=1
)
@click.option(
    "--task_set",
    help="Execute a task from specified task set(default: {0})".format(shdw.config.settings._TASK_SPEC_NAME),
    type=click.Choice([*shdw.plugin.get_tasks()]),
    default=shdw.config.settings._TASK_SPEC_NAME 
)
@click.option(
    "-t",
    "--task",
    help="Execute the specified task (default: {0})".format(""),
    type=str,
    default= shdw.config.settings._DEFAULT_TASK 
)
def cli(
        file,
        task_set,
        task,
    ):
    """Read general settings file and execute specified task."""

    # read general settings file and assign content to global settings object
    shdw.config.settings.get_settings(file)

    # get the specified task and imort it as module
    task_module = shdw.plugin.get_task_module(task_set)

    # call task's main routine
    if not task:
        shdw.__init__._logger.debug("Call the default routine from task set '{0}'".format(task_module[0]))
        task_module[0].main()
    else:
        shdw.__init__._logger.debug("Call task '{0}' from set '{1}'".format(task_module[0], task))

        task_funcs = shdw.plugin.get_module_functions(task_module[0])
        if not task in task_funcs:
            raise shdw.debug.exceptions.ArgumentError(task, task_funcs) 

        task_func = getattr(task_module[0], 
            "{}{}".format(shdw.config.settings._TASK_PREFIX, task)
        )
        task_func()