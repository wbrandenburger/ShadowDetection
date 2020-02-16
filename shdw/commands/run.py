# ===========================================================================
#   run.py ------------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import rsvis.__init__
import rsvis.config.settings
import rsvis.plugin

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
    "-t",
    "--task",
    help="Execute the specified task (default: {0})".format(rsvis.config.settings._DEFAULT_TASK),
    type=click.Choice([*rsvis.plugin.get_tasks()]), # @todo[to change]: folder "tasks"
    default=rsvis.config.settings._DEFAULT_TASK # @todo[to change]: default task "default"
)
@click.option(
    "-f",
    "--func",
    help="Execute the specified function (default: {0})".format(""),
    type=str,
    default= ""
)
def cli(
        file,
        task,
        func,
    ):
    """Read general settings file and execute specified task."""

    # read general settings file and assign content to global settings object
    rsvis.config.settings.get_settings(file)

    # get the specified task and imort it as module
    task_module = rsvis.plugin.get_task_module(task)

    # call task's main routine
    if not func:
        rsvis.__init__._logger.debug("Call the main routine from task module '{0}'".format(task_module[0]))
        task_module[0].main()
    else:
        rsvis.__init__._logger.debug("Call '{0}' from task module '{1}'".format(task_module[0], func))

        task_funcs = rsvis.plugin.get_module_functions(task_module[0], "^test")
        if not func in task_funcs:
            raise ValueError("Error: Invalid value for '-f' / '--func': invalid choice: {0}. (choose from {1})".format(
                func, 
                task_funcs
                )
            ) # @todo[generalize]: also in expmgmt

        task_func = getattr(task_module[0], func)
        task_func()