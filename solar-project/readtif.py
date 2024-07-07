import rioxarray
import xarray
from itertools import product
import os
import shutil
from glob import glob
from vendors.logger import init_logger
import logging
import toml

_FILE_NAME = "readtif"
# Load environment variable
BASE_PATH = os.environ["BASE_PATH"]
DATA_PATH = os.environ["DATA_PATH"]
# Load configuration
_CONFIG_PATH = os.path.join(BASE_PATH, 'config.toml')
with open(_CONFIG_PATH, "r") as f:
    config = toml.load(f)[_FILE_NAME]
TILE_SIZE = config["tile_size"]
STEP_SIZE = config["step_size"]
NAME_FORMAT = config["name_format"]
_LIST_NAME_FORMAT = NAME_FORMAT.split("_")
OUTPUT_PATH = config["output_path"]
STOP_IF_NOT_DIVISIBLE = config["stop_if_not_divisible"]
NAME_MODE = config["name_mode"]
_valid_name_mode = {'gps','pixel'}
if(NAME_MODE not in _valid_name_mode):
    raise ValueError(f"name_mode={NAME_MODE} can only be {_valid_name_mode} only")


init_logger(name=_FILE_NAME, filename=_FILE_NAME)
_logger = logging.getLogger(_FILE_NAME)

def search_tif(data_path:str) -> list[str]:
    """
    Lookup for all files inside the `data_path` and return as a `list[path]`
    """
    if(os.path.exists(data_path) == False):
        raise FileExistsError(f"The {data_path=} is not exist.")
    
    filenames = glob( os.path.join(data_path,'*') )
    _logger.info(msg=f"Found {len(filenames)} files")
    return filenames

def open_tif(path:str) -> xarray.DataArray:
    if(os.path.exists(path) == False):
        raise FileNotFoundError(f"The {path=} is not exist.")

    dataArray = rioxarray.open_rasterio(path)
    
    if(isinstance(dataArray, xarray.DataArray) == False):
        raise TypeError(f"Expect the tif file to load as 'xarray.DataArray' but got '{type(dataArray)}'")
    
    return dataArray

def _create_name_from_fmtdict(fmtdict:dict) -> str:
    name = ""
    name = ""
    for fmt in _LIST_NAME_FORMAT:
        name = f"{name}_{fmtdict[fmt]}"
    name = name.lstrip("_")
    return name

def spilt_tif(tif:xarray.DataArray, filepath:str):
    _, filename_ext = os.path.split(filepath)
    filename, _ = os.path.splitext(filename_ext)
    fmtdict = {
        "filename":filename,
        "xmin": None,
        "xmax": None,
        "ymin": None,
        "ymax": None
    }
    _, ysize, xsize = tif.shape
    
    path = os.path.join(BASE_PATH,DATA_PATH,OUTPUT_PATH,filename)
    if(os.path.exists(path) == False):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        # os.removedirs(path)
        os.makedirs(path)

    _MOVING_SIZE = TILE_SIZE * STEP_SIZE
    if(_MOVING_SIZE.is_integer() == False):
        raise ValueError(f"expect `TILE_SIZE * STEP_SIZE`=`{TILE_SIZE}*{STEP_SIZE}` to be integer but got {_MOVING_SIZE}")
    _MOVING_SIZE = int(_MOVING_SIZE)

    # Check divisible
    if(STOP_IF_NOT_DIVISIBLE):
        ypieces:float = ysize / TILE_SIZE
        xpieces:float = xsize / TILE_SIZE
        if( ypieces.is_integer() == False or xpieces.is_integer() == False ):
            raise ValueError(f"Becuase {STOP_IF_NOT_DIVISIBLE=}, the {TILE_SIZE=} can not devide {xsize=} or {ysize=}")

    for ypt, xpt in product(range(0,ysize,_MOVING_SIZE), range(0,xsize,_MOVING_SIZE)):
        ymin, ymax = ypt, ypt + TILE_SIZE
        xmin, xmax = xpt, xpt + TILE_SIZE
        if(ymax > ysize):
            ymax = ysize - 1
        if(xmax > xsize):
            xmax = xsize - 1

        if(NAME_MODE == 'pixel'):
            fmtdict["xmin"] = xmin
            fmtdict["xmax"] = xmax
            fmtdict["ymin"] = ymin
            fmtdict["ymax"] = ymax
        elif(NAME_MODE == 'gps'):
            fmtdict["xmin"] = float(tif.x[xmin].values)
            fmtdict["xmax"] = float(tif.x[xmax].values)
            fmtdict["ymin"] = float(tif.y[ymin].values)
            fmtdict["ymax"] = float(tif.y[ymax].values)
        else:
            raise ValueError(f"This should not happen. {NAME_MODE=} is invalid.")
        
        name = _create_name_from_fmtdict(fmtdict=fmtdict)
        temp = tif[:,ymin:ymax,xmin:xmax]
        temp.rio.to_raster(f"{path}/{name}.tif")
def process_tif(path:str):
    """
    take path of a tif file.
    1. open the tif with rioxarray
    2. get the crs
    3. get the split size from config
    4. split tif to tiles
    """
    # 1. open the tif with rioxarray
    xds = open_tif(path=path)
    # 2. get the crs
    crs = xds.rio.crs
    shape = xds.shape
    _logger.info(f"{path=} has {crs=}, {shape=}")
    # 3. get the split size from config
    # 4. split tif to tiles
    spilt_tif(tif=xds, filepath=path)

if __name__ == "__main__":
    # filename = 'watcharapol1.tif'
    path = os.path.join(BASE_PATH, DATA_PATH, "satellites")
    paths = search_tif(data_path=path)
    tifs = []
    for path in paths:
        process_tif(path)
    
