import os
from ipaddress import IPv4Interface
from pathlib import Path
from typing import List

import yaml
from jinja2 import Environment, FileSystemLoader

from src.config_base import ConfigBase


class ConfigAnsibleMssql(ConfigBase):
    __validation_data = [
        {
            "variable": "mssql_pid",
            "variable_description": "MSSQL product ID",
            "type": lambda x: isinstance(x, str),
            "type_description": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "mssql_pcs_cluster_vip_cidr",
            "variable_description": "MSSQL Pacemaker VIP",
            "type": lambda x: isinstance(x, IPv4Interface),
            "type_name": "IPv4Interface",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "mssql_accept_eula",
            "variable_description": "MSSQL EULA acceptance",
            "type": lambda x: isinstance(x, bool),
            "type_name": "bool",
            "value": lambda x: x,
            "value_description": "true",
        },
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Template
        self.template = "templates/settings-mssql.yml.jinja2"

        # Mssql
        self.mssql_pid = None
        self.mssql_pcs_cluster_vip_cidr = None
        self.mssql_accept_eula = False

        self.load(kwargs)

    def load(self, data: dict):
        if not isinstance(data, dict):
            raise ValueError(f"Parameter 'data' is not of type 'dict'")

        def to_ipv4interface(x: str):
            return IPv4Interface(x) if x is not None else None

        self.mssql_pid = data.get("mssql_pid")
        self.mssql_pcs_cluster_vip_cidr = to_ipv4interface(
            data.get("mssql_pcs_cluster_vip_cidr")
        )
        self.mssql_accept_eula = data.get("mssql_accept_eula", False)

    def open(self, file: str):
        # Load ansible file
        with open(file, "r") as file:
            data = yaml.safe_load(file).get("all", {}).get("vars", {})
        self.load(data)

    def write(self, file: str):
        j2_env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
            trim_blocks=True,
        )
        config = j2_env.get_template(self.template).render(
            mssql_pid=self.mssql_pid,
            mssql_pcs_cluster_vip_cidr=self.mssql_pcs_cluster_vip_cidr,
            mssql_accept_eula=self.mssql_accept_eula,
        )

        # Create config folder
        config_file = Path(file)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Save config to file
        with config_file.open(mode="w", encoding="utf-8") as f:
            f.write(config)

    def validate(self) -> List[str]:
        errors = self._check_validation_data(self.__validation_data)
        return [f"[Ansible]: {x}" for x in errors]

    @property
    def mssql_pid(self) -> str:
        return self.__pid

    @mssql_pid.setter
    def mssql_pid(self, value: str):
        # Todo: need to add regex pattern match for product key
        if value and value.lower() not in [
            "evaluation",
            "developer",
            "express",
            "web",
            "standard",
            "enterprise",
        ]:
            raise ValueError(f"MSSQL product ID is not valid: '{value}'")
        self.__pid = value

    @property
    def mssql_accept_eula(self) -> bool:
        return self.__accept_eula

    @mssql_accept_eula.setter
    def mssql_accept_eula(self, value: str):
        if not isinstance(value, bool):
            raise ValueError(f"Accept EULA is not of type 'bool': '{value}'")
        self.__accept_eula = value

    @property
    def mssql_pcs_cluster_vip_cidr(self) -> IPv4Interface:
        return self.__pcs_cluster_vip

    @mssql_pcs_cluster_vip_cidr.setter
    def mssql_pcs_cluster_vip_cidr(self, value: IPv4Interface):
        if value is not None and not isinstance(value, IPv4Interface):
            raise ValueError(
                f"PCS cluster VIP is not of type 'IPv4Interface': '{value}'"
            )
        self.__pcs_cluster_vip = value
