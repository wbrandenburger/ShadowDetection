# ===========================================================================
#   yaml.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import logging
import os
import yaml

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger("yaml")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def data_to_yaml(path, data):
    """
    Save data to yaml at path outpath

    :param yaml_path: Path to a yaml file
    :type  yaml_path: str

    :param data: Data in a dictionary
    :type  data: dict
    """
    with open(path, 'w+') as f:
        yaml.dump(
            data,
            f,
            #allow_unicode=True/False),
            default_flow_style=False,
            sort_keys=False
        )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def yaml_to_data(path, raise_exception=False):
    """
    Convert a yaml file into a dictionary using the yaml module.

    :param path: Path to a yaml file
    :type  path: str

    :return:: Dictionary containing the info of the yaml file
    :rtype:  dict

    :raises ValueError: If a yaml parsing error happens
    """
    if os.path.exists(path):
        return file_to_data(path, raise_exception=raise_exception)
    else:
        return string_to_data(path, raise_exception=raise_exception)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def file_to_data(path, raise_exception=False):
    """
    Convert a yaml file into a dictionary using the yaml module.

    :param path: Path to a yaml file
    :type  path: str

    :return:: Dictionary containing the info of the yaml file
    :rtype:  dict

    :raises ValueError: If a yaml parsing error happens
    """
    with open(path) as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            if raise_exception:
                raise ValueError(e)
            logger.error("Yaml syntax error: \n\n{0}".format(e))
            return dict()
        else:
            return data

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def string_to_data(string, raise_exception=False):
    """
    Convert a yaml string into a dictionary using the yaml module.

    :param string: string representation of dictionary
    :type string: str

    :return:: Dictionary containing the info of the string
    :rtype:  dict

    :raises ValueError: If a yaml parsing error happens
    """
    try:
        data = yaml.safe_load(string)
    except Exception as e:
        if raise_exception:
            raise ValueError(e)
        logger.error("Yaml syntax error: \n\n{0}".format(e))
        return dict()
    else:
        return data