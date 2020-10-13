"""A container to hold all configurations.

Config contains methods to read a yaml file and create an object to hold the configration. Once initialized, we can use the dot notation to access the configurations.

E.g.,
Let's say we have a yaml file called conf.yml

foo:
    bar: "bar"
    baz:
        baza: 1
        bazb: False

After reading this, we can use it as

>>> conf = Config("conf.yml")
>>> conf = conf.load_config()
>>> print(conf.bar)
bar
>>> print(conf.baz.baza)
1
>>> print(conf.baz.bazb)
False
"""
from __future__ import annotations
import os
import sys
import yaml
from pathlib import Path
from typing import Any, Tuple, Dict, List

# Add the main project path to the python path.
root = Path.cwd()
while root.name != "src":
    root = root.parent

if root not in sys.path:
    sys.path.append(str(root))


__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0"


class Config:
    def __init__(self, config_file: str = None) -> None:
        self.config_file = config_file
        self._num_attributes = 0

    def __iter__(self) -> Tuple[str, Any]:
        """
        Iterates over all the attributes.

        Yields
        ------
        (attr_name, attr_val): Tuple[str, ConfigBuilder or dict_like]
            Key is the name of the attribute. Value is either an instance of the 
        """
        for attr_name, attr_val in self.__dict__.items():
            yield attr_name, attr_val

    def get_num_attributes(self) -> int:
        """
        A getter method for number of attributes
        """
        return self._num_attributes

    def set_config(self, key: str, val: Any) -> Config:
        """
        Set config attribute

        Parameters
         ----------
        key: str
            Name of the config
        val: any
            The value
        """
        # If the config file is nested, then recurse.
        if isinstance(val, dict):
            cfg_cls = Config()
            for sub_key, sub_val in val.items():
                cfg_cls = cfg_cls.set_config(sub_key, sub_val)
            val = cfg_cls

        self._num_attributes += 1
        setattr(self, key, val)
        return self

    def load_config(self) -> Config:
        """
        Read a yaml file with all the configurations and set them.

        Parameters
         ----------
        config_file: path_str
            Path to the config yaml file

        Returns
        -------
        self: self
            A reference to self
        """
        with open(self.config_file, 'r') as cfg:
            yaml_loader = yaml.load(cfg, Loader=yaml.FullLoader)
            for attr_name, attr_val in yaml_loader.items():
                self.set_config(attr_name, attr_val)

        return self