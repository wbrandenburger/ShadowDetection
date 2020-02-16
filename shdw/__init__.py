# ===========================================================================
#   __init__.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import logging
import os

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
__license__ = "MIT"
__version__ = '0.1'
__author__ = __maintainer__ = "Wolfgang Brandenburger"
__email__ = "wolfgang.brandenburger@outlook.com"

#   script ------------------------------------------------------------------
# ---------------------------------------------------------------------------
try:
    import colorama
    colorama.init()

    log_format = (
        'File "%(pathname)s", line %(lineno)s:\n' +
        colorama.Fore.YELLOW +
        '%(levelname)s' +
        ':' +
        colorama.Fore.GREEN +
        '%(name)s' +
        colorama.Fore.CYAN +
        ':' +
        '%(message)s' +
        colorama.Style.RESET_ALL
    )

    logging.basicConfig(format=log_format)

    _logger = logging.getLogger("shdw")

    if os.environ.get("SHDWDEBUG"):
        _logger.setLevel(logging.DEBUG)
        
except ImportError:
    pass
