from pathlib import Path
from decouple import config as decouple_config, Config, RepositoryEnv
from functools import lru_cache



PROJECT_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = PROJECT_DIR / ".env"


#? "lru_cache" won't be reloaded everytime
@lru_cache
def get_config():
    if ENV_FILE_PATH.exists():
        return Config(RepositoryEnv(ENV_FILE_PATH))
    return decouple_config


config = get_config()