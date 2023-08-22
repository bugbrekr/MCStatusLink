import multiprocessing
import toml
import os

_config = toml.load("config/config.toml")

bind = _config['bind']
workers = _config['workers']