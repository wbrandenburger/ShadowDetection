# ===========================================================================
#   test.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.config.settings
import shdw.utils.format

import shdw.tools.experiments

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def main():
    
    test_user_data()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_shadow_freitas():
    shdw.tools.experiments.get_shadow_freitas(
        shdw.config.settings._DATA,
        shdw.config.settings._SETTINGS["io"]["dest-dir"],
        shdw.config.settings._SETTINGS["io"]["dest-basename"],
        shdw.config.settings._SETTINGS["io"]["regex"]
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_shadow_silva():
    shdw.tools.experiments.get_shadow_silva(
        shdw.config.settings._DATA,
        shdw.config.settings._SETTINGS["io"]["dest-dir"],
        shdw.config.settings._SETTINGS["io"]["dest-basename"],
        shdw.config.settings._SETTINGS["io"]["regex"]
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_research():
    import shdw.utils.regex
    research = shdw.utils.regex.ReSearch(*shdw.config.settings._SETTINGS["io"]["regex"])
    print(research("A:\\Blubb\\ABC_345_RGB.tif"))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_user_settings():
    """Print the user settings"""
    
    # print user's defined settings
    shdw.__init__._logger.info("Print user's defined settings")
    shdw.utils.format.print_data(shdw.config.settings._SETTINGS)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def test_user_data():
    """Print the user data"""
    
    # print user's defined data
    shdw.__init__._logger.info("Print user's defined data")
    shdw.utils.format.print_data(shdw.config.settings._DATA)