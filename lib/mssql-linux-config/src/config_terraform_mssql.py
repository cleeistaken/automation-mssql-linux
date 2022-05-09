import os
import hcl2

from ipaddress import IPv4Network, IPv4Address
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from .config_base import ConfigBase
from .utils import find_duplicates
from .vcenter_server import VCenterServer


class ConfigTerraformMssql(ConfigBase):

    __validation_data = [
        {
            "variable": "template",
            "variable_description": "jinja2 template",
            "type": lambda x: isinstance(x, str),
            "type_description": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vcenter_server",
            "variable_description": "vCenter host",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vcenter_user",
            "variable_description": "vCenter username",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vcenter_password",
            "variable_description": "vCenter password",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
        },
        {
            "variable": "vcenter_insecure_ssl",
            "variable_description": "vCenter allow insecure SSL",
            "type": lambda x: isinstance(x, bool),
            "type_name": "bool",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_datacenter",
            "variable_description": "vSphere datacenter",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_compute_cluster",
            "variable_description": "vSphere cluster",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_datastore",
            "variable_description": "vSphere datastore",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_network_1_portgroup",
            "variable_description": "vSphere portgroup 1",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_network_1_ipv4_subnet_cidr",
            "variable_description": "IPv4 network 1 subnet",
            "type": lambda x: isinstance(x, IPv4Network),
            "type_name": "IPv4Network",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_network_1_ipv4_gateway",
            "variable_description": "IPv4 network 1 gateway",
            "type": lambda x: isinstance(x, IPv4Address),
            "type_name": "IPv4Address",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vsphere_network_1_ipv4_ips",
            "variable_description": "IPv4 network 1 IP addresses",
            "type": lambda x: (
                isinstance(x, List) and all(isinstance(y, IPv4Address) for y in x)
            ),
            "type_name": "List[IPv4Address]",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "network_ipv4_dns_servers",
            "variable_description": "IPv4 DNS servers",
            "type": lambda x: (
                isinstance(x, List) and all(isinstance(y, IPv4Address) for y in x)
            ),
            "type_name": "List[IPv4Address]",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "network_domain_name",
            "variable_description": "Domain name",
            "type": lambda x: isinstance(x, str),
            "type_name": "str",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "network_dns_suffix",
            "variable_description": "Domain suffixes",
            "type": lambda x: isinstance(x, list)
            and all(isinstance(y, str) for y in x),
            "type_name": "List[str]",
            "value": None,
            "value_description": None,
        },
        {
            "variable": "vm_mssql_count",
            "variable_description": "MSSQL VM count",
            "type": lambda x: isinstance(x, int),
            "type_name": "int",
            "value": lambda x: (0 < x < 16),
            "value_description": "in the range of [1, 15]",
        },
        {
            "variable": "vm_mssql_vcpu_count",
            "variable_description": "MSSQL VM vCPU count",
            "type": lambda x: isinstance(x, int),
            "type_name": "int",
            "value": lambda x: (2 < x < 128),
            "value_description": "in the range of [2, 128]",
        },
        {
            "variable": "vm_mssql_memory_gb",
            "variable_description": "MSSQL VM memory size",
            "type": lambda x: isinstance(x, int),
            "type_name": "int",
            "value": lambda x: (4 < x < 1024),
            "value_description": "in the range of [4, 1024]",
        },
        {
            "variable": "vm_mssql_data_disk_gb",
            "variable_description": "MSSQL VM data disk size",
            "type": lambda x: isinstance(x, int),
            "type_name": "int",
            "value": lambda x: (x >= 40),
            "value_description": "greater than 40",
        },
        {
            "variable": "vm_mssql_log_disk_gb",
            "variable_description": "MSSQL VM log disk size",
            "type": lambda x: isinstance(x, int),
            "type_name": "int",
            "value": lambda x: (x >= 10),
            "value_description": "greater than 10",
        },
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Template
        self.template = "templates/terraform-mssql.tfvars.jinja2"

        # vCenter
        self.vcenter_server = None
        self.vcenter_user = None
        self.vcenter_password = None
        self.vcenter_insecure_ssl = None

        # vSphere
        self.vsphere_datacenter = None
        self.vsphere_compute_cluster = None
        self.vsphere_datastore = None

        # vSphere network
        self.vsphere_network_1_portgroup = None
        self.vsphere_network_1_ipv4_subnet_cidr = None
        self.vsphere_network_1_ipv4_gateway = None
        self.vsphere_network_1_ipv4_ips = None

        # Network
        self.network_ipv4_dns_servers = None
        self.network_domain_name = None
        self.network_dns_suffix = None

        # MSSQL VM
        self.vm_mssql_count = None
        self.vm_mssql_vcpu_count = None
        self.vm_mssql_memory_gb = None
        self.vm_mssql_data_disk_gb = None
        self.vm_mssql_log_disk_gb = None

        self.load(kwargs)

    def load(self, data: dict):
        if not isinstance(data, dict):
            raise ValueError(f"Parameter 'data' is not of type 'dict'")

        def to_ipv4network(x: str):
            return IPv4Network(x) if x is not None else None

        def to_ipv4address(x: str):
            return IPv4Address(x) if x is not None else None

        def to_ipv4address_list(x: List[str]):
            return [IPv4Address(y) for y in x] if x is not None else None

        # vCenter
        self.vcenter_server = data.get("vcenter_server")
        self.vcenter_user = data.get("vcenter_user")
        self.vcenter_password = data.get("vcenter_password")
        self.vcenter_insecure_ssl = data.get("vcenter_insecure_ssl")

        # vSphere
        self.vsphere_datacenter = data.get("vsphere_datacenter")
        self.vsphere_compute_cluster = data.get("vsphere_compute_cluster")
        self.vsphere_datastore = data.get("vsphere_datastore")

        # vSphere network
        self.vsphere_network_1_portgroup = data.get("vsphere_network_1_portgroup")
        self.vsphere_network_1_ipv4_subnet_cidr = to_ipv4network(
            data.get("vsphere_network_1_ipv4_subnet_cidr")
        )
        self.vsphere_network_1_ipv4_gateway = to_ipv4address(
            data.get("vsphere_network_1_ipv4_gateway")
        )
        self.vsphere_network_1_ipv4_ips = to_ipv4address_list(
            data.get("vsphere_network_1_ipv4_ips")
        )

        # Network
        self.network_ipv4_dns_servers = to_ipv4address_list(
            data.get("network_ipv4_dns_servers")
        )
        self.network_domain_name = data.get("network_domain_name")
        self.network_dns_suffix = data.get("network_dns_suffix")

        # MSSQL VM
        self.vm_mssql_count = data.get("vm_mssql_count")
        if "vm_mssql" in data:
            self.vm_mssql_vcpu_count = data.get("vm_mssql").get("cpu")
            self.vm_mssql_memory_gb = data.get("vm_mssql").get("memory_gb")
            self.vm_mssql_data_disk_gb = data.get("vm_mssql").get("data_disk_gb")
            self.vm_mssql_log_disk_gb = data.get("vm_mssql").get("log_disk_gb")
        else:
            self.vm_mssql_vcpu_count = None
            self.vm_mssql_memory_gb = None
            self.vm_mssql_data_disk_gb = None
            self.vm_mssql_log_disk_gb = None

    def open(self, file: str):
        with open(file, "r") as file:
            data = hcl2.load(file)
        self.load(data)

    def write(self, file: str):
        j2_env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
            trim_blocks=True,
        )
        config = j2_env.get_template(self.template).render(
            vcenter_server=self.vcenter_server,
            vcenter_user=self.vcenter_user,
            vcenter_password=self.vcenter_password,
            vcenter_insecure_ssl=self.vcenter_insecure_ssl,
            vsphere_datacenter=self.vsphere_datacenter,
            vsphere_compute_cluster=self.vsphere_compute_cluster,
            vsphere_datastore=self.vsphere_datastore,
            vsphere_network_1_portgroup=self.vsphere_network_1_portgroup,
            vsphere_network_1_ipv4_subnet_cidr=self.vsphere_network_1_ipv4_subnet_cidr,
            vsphere_network_1_ipv4_ips=self.vsphere_network_1_ipv4_ips,
            vsphere_network_1_ipv4_gateway=self.vsphere_network_1_ipv4_gateway,
            network_ipv4_dns_servers=self.network_ipv4_dns_servers,
            network_domain_name=self.network_domain_name,
            network_dns_suffix=self.network_dns_suffix,
            vm_mssql_count=self.vm_mssql_count,
            vm_mssql_vcpu_count=self.vm_mssql_vcpu_count,
            vm_mssql_memory_gb=self.vm_mssql_memory_gb,
            vm_mssql_data_disk_gb=self.vm_mssql_data_disk_gb,
            vm_mssql_log_disk_gb=self.vm_mssql_log_disk_gb,
        )

        # Create config folder
        config_file = Path(file)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Save config to file
        with config_file.open(mode="w", encoding="utf-8") as f:
            f.write(config)

    def validate_network(self) -> List[str]:
        """This validates if network 1 values are valid."""
        errors = []

        # User short name variables to make the code more readable
        subnet = self.vsphere_network_1_ipv4_subnet_cidr
        gateway = self.vsphere_network_1_ipv4_gateway
        ips = self.vsphere_network_1_ipv4_ips

        # Gateway subnet
        if subnet and gateway:
            if self.verbose:
                print(f"Checking if gateway is in the defined network... ", end="")
            if gateway in subnet:
                if self.verbose:
                    print("OK")
            else:
                if self.verbose:
                    print("ERROR")
                errors.append(
                    f"IPv4 gateway is not in the defined network: '{gateway}' not in '{subnet}'"
                )

        # Duplicate IP
        if ips:
            if self.verbose:
                print(f"Checking for duplicate IP... ", end="")
            if len(set(ips)) == len(ips):
                if self.verbose:
                    print("OK")
            else:
                if self.verbose:
                    print("ERROR")
                dupes = ", ".join([str(x) for x in find_duplicates(ips)])
                errors.append(f"IPv4 IP list has duplicate entries: '{dupes}'")

        # IP subnet
        if subnet and ips:
            if self.verbose:
                print(f"Checking for invalid IP entries... ", end="")
            invalid_ips = [str(x) for x in ips if x not in subnet]
            if invalid_ips:
                if self.verbose:
                    print("ERROR")
                errors.append(f"IP not in network subnet: {', '.join(invalid_ips)}")
            else:
                if self.verbose:
                    print("OK")

        return errors

    def validate_misc(self) -> List[str]:
        errors = []

        # Number of IP
        if self.vm_mssql_count and self.vsphere_network_1_ipv4_ips:
            if self.verbose:
                print(f"Checking the number of IP required... ", end="")

            # variable to make the code more readable
            required = self.vm_mssql_count
            actual = len(self.vsphere_network_1_ipv4_ips)

            if required <= actual:
                if self.verbose:
                    print("OK")
            else:
                if self.verbose:
                    print("ERROR")
                errors.append(
                    f"Need '{required}' IP in 'vsphere_network_1_ipv4_ips' but only '{actual}' defined."
                )
        return errors

    def validate_vsphere(self) -> List[str]:
        """This validates if the vSphere values are valid."""
        errors = []

        # Check vSphere resources
        if not (
            self.vcenter_server
            and self.vcenter_user
            and self.vcenter_password
            and self.vcenter_insecure_ssl
        ):
            # Can't check if we can't connect...
            return errors

        if self.verbose:
            print("Checking if the vSphere parameters are valid.")

        try:
            with VCenterServer(
                host=self.vcenter_server,
                username=self.vcenter_user,
                password=self.vcenter_password,
                allow_insecure_ssl=self.vcenter_insecure_ssl,
            ) as vc_server:

                # Check datacenter
                if self.verbose:
                    print(
                        f"Checking if datacenter '{self.vsphere_datacenter}' exists... ",
                        end="",
                    )
                vc_datacenter = vc_server.find_datacenter(self.vsphere_datacenter)
                if vc_datacenter:
                    if self.verbose:
                        print("OK")
                else:
                    if self.verbose:
                        print("ERROR")
                    errors.append(
                        f"Could not find datacenter '{self.vsphere_datacenter}' in '{self.vcenter_server}'"
                    )
                    return errors

                # Check cluster
                if self.verbose:
                    print(
                        f"Checking if cluster '{self.vsphere_compute_cluster}' exists... ",
                        end="",
                    )
                vc_cluster = vc_datacenter.find_cluster(self.vsphere_compute_cluster)
                if vc_cluster:
                    if self.verbose:
                        print("OK")
                else:
                    if self.verbose:
                        print("ERROR")
                    errors.append(
                        f"Could not find cluster: '{self.vsphere_compute_cluster}' in '{self.vsphere_datacenter}'"
                    )
                    return errors

                # Check datastore
                if self.verbose:
                    print(
                        f"Checking if datastore '{self.vsphere_datastore}' exists... ",
                        end="",
                    )
                vc_datastore = vc_cluster.find_datastore(self.vsphere_datastore)
                if vc_datastore:
                    if self.verbose:
                        print("OK")
                else:
                    if self.verbose:
                        print("ERROR")
                    errors.append(
                        f"Could not find datastore: '{self.vsphere_datastore}' in '{self.vsphere_compute_cluster}'"
                    )
                    return errors

                # Check network
                if self.verbose:
                    print(
                        f"Checking if portgroup '{self.vsphere_network_1_portgroup}' exists... ",
                        end="",
                    )
                vc_network = vc_cluster.find_network(self.vsphere_network_1_portgroup)
                if vc_network:
                    if self.verbose:
                        print("OK")
                else:
                    if self.verbose:
                        print("ERROR")
                    pg = self.vsphere_network_1_portgroup
                    cluster = self.vsphere_compute_cluster
                    errors.append(f"Could not find network: '{pg}' in '{cluster}'")
                    return errors

                # Hosts
                for host in vc_cluster.hosts:
                    if self.verbose:
                        print(f"Checking host '{host.name}'")

                    if self.verbose:
                        print("Checking datastore... ", end="")
                    if host.find_datastore(self.vsphere_datastore):
                        if self.verbose:
                            print("OK")
                    else:
                        if self.verbose:
                            print("ERROR")
                        errors.append(
                            f"Datastore {self.vsphere_datastore} not on host {host.name}."
                        )

                    if self.verbose:
                        print("Checking portgroup... ", end="")
                    if host.find_network(self.vsphere_network_1_portgroup):
                        if self.verbose:
                            print("OK")
                    else:
                        if self.verbose:
                            print("ERROR")
                        errors.append(
                            f"Portgroup {self.vsphere_network_1_portgroup} not on host {host.name}."
                        )

        except ValueError as e:
            errors.append(f"Unable to connect to vCenter: {e}")

        return errors

    def validate(self) -> List[str]:
        errors = self._check_validation_data(self.__validation_data)
        errors.extend(self.validate_network())
        errors.extend(self.validate_misc())
        errors.extend(self.validate_vsphere())
        return [f"[Terraform]: {x}" for x in errors]

    @property
    def vsphere_network_1_ipv4_subnet_cidr(self) -> IPv4Network:
        return self.__vsphere_network_1_ipv4_subnet

    @vsphere_network_1_ipv4_subnet_cidr.setter
    def vsphere_network_1_ipv4_subnet_cidr(self, value: IPv4Network):
        if value is not None and not isinstance(value, IPv4Network):
            raise ValueError(
                f"Value for 'vsphere_network_1_ipv4_subnet' is not of type 'IPv4Network'"
            )
        self.__vsphere_network_1_ipv4_subnet = value

    @property
    def network_ipv4_dns_servers(self) -> List[IPv4Address]:
        return self.__network_ipv4_dns_servers

    @network_ipv4_dns_servers.setter
    def network_ipv4_dns_servers(self, value: List[IPv4Address]):
        if value is not None:
            if not isinstance(value, List):
                raise ValueError(
                    "Value for 'vsphere_network_1_ipv4_dns' is not of type 'List'"
                )
            if not all(type(n) is IPv4Address for n in value):
                raise ValueError(
                    f"Item in 'vsphere_network_1_ipv4_dns' list is not of type 'IPv4Address'"
                )
        self.__network_ipv4_dns_servers = value

    @property
    def vsphere_network_1_ipv4_gateway(self) -> IPv4Address:
        return self.__vsphere_network_1_ipv4_gateway

    @vsphere_network_1_ipv4_gateway.setter
    def vsphere_network_1_ipv4_gateway(self, value: IPv4Address):
        if not isinstance(value, IPv4Address) and value is not None:
            raise ValueError(
                f"Value for 'vsphere_network_1_ipv4_gateway' is not of type 'IPv4Address'"
            )
        self.__vsphere_network_1_ipv4_gateway = value

    @property
    def vsphere_network_1_ipv4_ips(self) -> List[IPv4Address]:
        return self.__vsphere_network_1_ipv4_ips

    @vsphere_network_1_ipv4_ips.setter
    def vsphere_network_1_ipv4_ips(self, value: List[IPv4Address]):
        if value is not None:
            if not isinstance(value, List):
                raise ValueError(
                    "Value for 'vsphere_network_1_ipv4_ips' is not of type List"
                )
            if not all(type(n) is IPv4Address for n in value):
                raise ValueError(
                    "Value for item in 'vsphere_network_1_ipv4_ips' is not of type 'IPv4Address'"
                )
        self.__vsphere_network_1_ipv4_ips = value
