# ===========================================================================
#   exceptions.py -----------------------------------------------------------
# ===========================================================================

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class ArgumentError(Exception):
    """This exception is when a argument's value does not coincide with the items of a predefined list.
    """
    def __init__(self, arg, arg_list):
        message = """

    The input argument '{0}' is a invalid choice. Choose from: {1} 
        """.format(arg, arg_list)
        super(ArgumentError, self).__init__(message)

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class KeyErrorJson(Exception):
    """This exception is when a key is missing in a json file.
    """

    def __init__(self, key):
        message = """

    The key {0} is not defined in the settings. Try setting its value in 
    your settings file as such:

        {{
            "{0}" : "..."
        }}

        """.format(key)
        super(KeyErrorJson, self).__init__(message)