"""
This modules is for loading the configuration of this package
"""

BASE_PATH:str = None
LOG_PATH :str = None
def _load_global(path:str):
    import toml
    conf = toml.load(path)['global']
    global BASE_PATH
    global LOG_PATH
    BASE_PATH = conf['base_path']
    LOG_PATH = conf['log_path']

_load_global("./config.toml")