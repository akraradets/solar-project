import os
import toml
from vendors.logger import init_logger
import logging
from solar.vars import *

_FILE_NAME="prepare_project"
_logger = init_logger(name=_FILE_NAME, filename=_FILE_NAME, path=LOG_PATH)

# Load configuration
_CONFIG_PATH = os.path.join(BASE_PATH, 'config.toml')
with open(_CONFIG_PATH, "r") as f:
    config = toml.load(f)[_FILE_NAME]

def _prepare_folders():
    for pfolder, subs in config.items():
        for sub in subs:
            path = os.path.join(pfolder, sub)
            if(os.path.exists(path) == False):
                os.makedirs(path)

def run():
    _prepare_folders()