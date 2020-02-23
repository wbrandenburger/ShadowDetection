# ===========================================================================
#   test.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
#import shdw.config.settings
#import shdw.utils.format

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_default():
    shdw.__init__._logger.warning("No task chosen from set 'tests'")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_test_dict_parser():
    import shdw.utils.dictparser
    obj = shdw.utils.dictparser.DictParser(shdw.config.settings._SETTINGS)
    obj.interpolate()
    print(dict(obj))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def task_test_research():
    import shdw.utils.general
    research = shdw.utils.general.ReSearch(*shdw.config.settings._SETTINGS["output"]["regex"])
    print(research("G:\\Blubb\\ABC_345_RGB.tif"))