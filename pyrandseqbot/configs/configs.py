""" This module contains settings containers. Different settings are stored in different containers, main access is
provided with `Configs` class help.
"""

import logging.config
from pathlib import Path
from typing import Any, Union

from pydantic import BaseModel
from ruamel.yaml import YAML

from pyrandseqbot.configs.environment import Config as EnvironmentConfig

__all__ = ['Context', 'ConfigsABC', 'PathConfigs', 'BotConfigs', 'DatabaseConfigs', 'Configs']


class Context(BaseModel):
    yml: Any
    env: Any
    package_dir: Path

    @classmethod
    def load(
        cls,
        package_dir: Union[str, Path],
        yml_path: Union[str, Path] = None,
        env_path: Union[str, Path] = None
    ) -> 'Context':
        """ Load configs from environment and YAML file """

        package_dir = Path(package_dir)
        if not package_dir.exists():
            raise FileNotFoundError(package_dir)

        env_path = Path(env_path or f'{package_dir.parent}/.env')
        env_config = EnvironmentConfig(env_path if env_path.exists() else '')

        yaml = YAML()
        yml_path = Path(yml_path or f'{package_dir}/configs/configs.yml')
        with yml_path.open('r', encoding='utf-8') as fp:
            yml_config = yaml.load(fp)
        return cls(yml=yml_config, env=env_config, package_dir=package_dir)


class ConfigsABC:
    def __init__(self, package_dir: Union[str, Path], **kwargs) -> None:
        self.context = Context.load(package_dir, **kwargs)

    @classmethod
    def from_package(cls, entrypoint: str, **kwargs) -> 'ConfigsABC':
        package_dir = Path(entrypoint).parent
        return cls(
            package_dir=package_dir,
            yml_path=package_dir / 'configs/configs.yml',
            env_path=package_dir.parent / '.env',
            **kwargs
        )


class PathConfigs(BaseModel):
    logs: Path


class BotConfigs(BaseModel):
    env: str
    host: str
    port: int
    token: str
    name: str

    @classmethod
    def from_context(cls, context: Context):
        return cls(
            env=context.env.get('ENV', default='dev'),
            host=context.env.get('HOST', default='localhost'),
            port=context.env.get('PORT', default=8443, cast=int),
            token=context.env.get('BOT_TOKEN'),
            name=context.env.get('BOT_NAME')
        )

    @property
    def webhook_url(self) -> str:
        return f'https://{self.host}/{self.token}'


class DatabaseConfigs(BaseModel):
    name: str
    connect_retry_count: int
    connect_retry_delay: int

    @classmethod
    def from_context(cls, context: Context) -> 'DatabaseConfigs':
        instance = cls(
            name=context.yml['db']['name'],
            connect_retry_count=context.yml['db']['connect_retry']['count'],
            connect_retry_delay=context.yml['db']['connect_retry']['delay']
        )
        Path(instance.name).parent.mkdir(exist_ok=True, parents=True)
        return instance

    @property
    def dsn(self) -> str:
        return f'sqlite:///{self.name}'


class Configs(ConfigsABC):
    """ Container of all system configs """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.path = PathConfigs(
            logs=Path(self.context.yml['path']['logs'])
        )
        self.path.logs.mkdir(parents=True, exist_ok=True)
        self.configure_logging()

        self.bot = BotConfigs.from_context(self.context)
        self.db = DatabaseConfigs.from_context(self.context)

    def configure_logging(self) -> 'Configs':
        """ Add logs directory path to all file handlers and apply logging configs """

        if 'handlers' in self.context.yml['logging']:
            for key in self.context.yml['logging']['handlers']:
                handler_fname = self.context.yml['logging']['handlers'][key].get('filename')
                if handler_fname:
                    self.context.yml['logging']['handlers'][key]['filename'] = f'{self.path.logs}/{handler_fname}'
        logging.config.dictConfig(self.context.yml['logging'])
        return self
