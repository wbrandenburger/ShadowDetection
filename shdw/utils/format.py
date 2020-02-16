# ===========================================================================
#   format.py ---------------------------------------------------------------
# ===========================================================================

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def print_data(data):
    """
    Print a formatted list of elements, tuples or a dictionary

    :param data: List of elements, tuples or a dictionary
    :type  data: list or dict
    """
    # create a list of tuples from the given dictionary and pass to printing
    if isinstance(data, dict):
        print_dict(data)
    elif isinstance(data, list):
        # print the items of the given list
        if not isinstance(data[0], tuple):
            print_list(data)
        else:
            print_table(data)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def print_dict(data):
    """
    Create a list of tuples from the given dictionary and pass to printing
    
    :param data: Dictionary
    :type  data: dict
    """
    assert(isinstance(data, dict))
    data = [(str(item), str(value)) for item, value in data.items()]
    print_table(data)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def print_list(data):
    """
    Print the items of the given list
    
    :param data: List
    :type  data: list
    """
    for item in data:
        if isinstance(item, dict):
            print_data(item)
        else:
            print(item)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def print_table(data):
    """
    Print the items of the given list with tuples of arbitrary size
    
    :param data: List of tuples
    :type  data: list
    """
    # get the maximum lenght of an tuples element in the list
    col_width = [max(len(x) for x in col) for col in zip(*data)]
    
    # loop through the list 
    for line in data:
        print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")
    print("")

