from dataclasses import dataclass
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

import sys
sys.path.append(base_dir)


@dataclass
class DevConfig():
    PROJ_RELOAD: bool = True
    DB_URL: str = "mongodb://USERID:USERPASS@IP:PORT/"
    DB_NAME: str = "dev"

@dataclass
class PrdConfig():
    PROJ_RELOAD: bool = False
    DB_URL: str = "mongodb://USERID:USERPASS@IP:PORT/"
    DB_NAME: str = "prd"

def conf():
    config = dict(prd=PrdConfig(), dev=DevConfig())
    return config.get(environ.get("API_ENV", "dev"))