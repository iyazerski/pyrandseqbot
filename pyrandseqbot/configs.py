import logging
import logging.config
from pathlib import Path

from pydantic import BaseModel
from ruamel.yaml import YAML
from starlette.config import Config

_logger = logging.getLogger(__name__)


class PathConfig(BaseModel):
    logs: Path = None
    db: Path = None
    basedir: Path = Path(__file__).parent.parent


class ApiConfig(BaseModel):
    token: str


class OrmConfig(BaseModel):
    connection_string: str


class Configs:
    def __init__(self, path: PathConfig = None, api: ApiConfig = None, orm: OrmConfig = None):
        self.path = path
        self.api = api
        self.orm = orm
        self.loaded = False

    def load(self, config_path: str = None) -> 'Configs':
        env_config = Config('.env')
        yaml = YAML()

        config_path = Path(config_path or f'{Path(__file__).parent}/configs.yml')
        with config_path.open('r', encoding='utf-8') as fp:
            yml_config = yaml.load(fp)
        base_dir = config_path.parent.parent

        self.path = PathConfig(
            **{key: Path(f'{base_dir}/{value}') for key, value in yml_config['path'].items()},
            base_dir=base_dir
        )
        self.path.logs.mkdir(parents=True, exist_ok=True)
        self.path.db.parent.mkdir(parents=True, exist_ok=True)
        self.api = ApiConfig(token=env_config.get('TELEGRAM_TOKEN', cast=str))
        self.orm = OrmConfig(connection_string=f'sqlite:///{configs.path.db}')

        if 'handlers' in yml_config['logging']:
            for key in yml_config['logging']['handlers']:
                handler_fname = yml_config['logging']['handlers'][key].get('filename')
                if handler_fname:
                    yml_config['logging']['handlers'][key]['filename'] = f'{self.path.logs}/{handler_fname}'
        logging.config.dictConfig(yml_config['logging'])

        self.loaded = True
        _logger.info('Configs successfully loaded')
        return self


configs = Configs()
