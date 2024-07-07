import logging
import logging.handlers as handlers
import sys
import os

BASE_PATH = os.environ["BASE_PATH"]
LOG_PATH  = os.environ["LOG_PATH"]
_path = os.path.join(BASE_PATH, LOG_PATH)

def init_logger(name:str, filename:str, path:str=_path, level:int=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file = os.path.join(path,f"{filename}.log")
    formatter = logging.Formatter('%(asctime)s|%(filename)s:%(funcName)s:%(lineno)d|%(levelname)s|%(message)s')
    formatter.datefmt = '%d-%m-%Y %H:%M:%S'
    # Handler
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    # fileHandler = logging.FileHandler(filename=file)
    # fileHandler.setFormatter(formatter)
    # This will rotate log
    fileHandler = handlers.RotatingFileHandler(filename=file, mode='a', maxBytes=10240000, backupCount=10)
    fileHandler.setFormatter(formatter)

    # Add Handler
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    logger.propagate = False