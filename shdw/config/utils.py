import os

def get_config_dirs():
    """Get rsvis configuration directories where the configuration
    files might be stored

    :return:: Folder where the configuration files might be stored
    :rtype:  list
    """
    dirs = []
    if os.environ.get('XDG_CONFIG_DIRS'):
        # get_config_home should also be included on top of XDG_CONFIG_DIRS
        dirs += [
            os.path.join(d, 'rsvis') for d in
            os.environ.get('XDG_CONFIG_DIRS').split(':')
        ]
    # Take XDG_CONFIG_HOME and ~/.rsvis for backwards
    # compatibility
    dirs += [
        os.path.join(get_config_home(), 'rsvis'),
        os.path.join(os.path.expanduser('~'), '.rsvis')
    ]
    return dirs

def get_config_folder():
    """Get folder where the configuration files are stored,
    e.g. ``~/rsvis``. It is XDG compatible, which means that if the
    environment variable ``XDG_CONFIG_HOME`` is defined it will use the
    configuration folder ``XDG_CONFIG_HOME/rsvis`` instead.

    :return:: Folder where the configuration files are stored
    :rtype:  str
    """
    config_dirs = get_config_dirs()
    for config_dir in config_dirs:
        if os.path.exists(config_dir):
            return config_dir
    # If no folder is found, then get the config home
    return os.path.join(get_config_home(), "rsvis")

def get_config_home():
    """Get the base directory relative to which user specific configuration
    files should be stored.

    :return:: Configuration base directory
    :rtype:  str
    """
    xdg_home = os.environ.get('XDG_CONFIG_HOME')
    if xdg_home:
        return os.path.expanduser(xdg_home)
    else:
        return os.path.join(os.path.expanduser('~'), '.config')

def get_scripts_folder():
    """Get folder where the scripts are stored,
    e.g. ~/.rsvis/scripts

    :return:: Folder where the scripts are stored
    :rtype:  str  
    """
    return os.path.join(
        get_config_folder(), "scripts"
    )
