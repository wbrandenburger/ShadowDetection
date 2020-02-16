# ===========================================================================
#   __main__.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.commands.run

import sys

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    """Main"""
    
    # log all retrieved arguments
    shdw.__init__._logger.debug("Number of arguments {0}:".format(len(sys.argv)))
    shdw.__init__._logger.debug("CLI-Arguments are: {0}".format(str(sys.argv)))

    # call default command line interface
    shdw.commands.run.cli()
