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
class DefaultExperimentMissing(Exception):
    """This exception is when a experiment has no name.
    """

    def __init__(self, name):
        message = """

    No experiment defined in the local settings file has
    the specified name '{0}'. Try setting its value in 
    your settings file as such:
    
    [
        {{
            name : {0}
        }}
    ]

    Don't forget to check the documentation.
        """.format(name)
        super(DefaultExperimentMissing, self).__init__(message)