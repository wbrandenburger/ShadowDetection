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