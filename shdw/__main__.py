# ===========================================================================
#   __main__.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import rsvis.__init__
import rsvis.commands.run

import sys

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    """Main"""
    
    # log all retrieved arguments
    rsvis.__init__._logger.debug("Number of arguments {0}:".format(len(sys.argv)))
    rsvis.__init__._logger.debug("CLI-Arguments are: {0}".format(str(sys.argv)))

    # call default command line interface
    rsvis.commands.run.cli()
