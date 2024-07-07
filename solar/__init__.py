BASE_PATH:str = None

def load_global(path:str):
    import toml
    conf = toml.load(path)['global']
    global BASE_PATH
    BASE_PATH = conf['base_path']

load_global("./config.toml")
