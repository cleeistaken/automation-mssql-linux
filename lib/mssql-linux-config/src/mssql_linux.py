from ipaddress import IPv4Network, IPv4Address, IPv4Interface

import inquirer

from inquirer.themes import GreenPassion
from pathlib import Path
from typing import List

from .config_base import ConfigBase
from src.config_ansible_mssql import ConfigAnsibleMssql
from src.config_terraform_mssql import ConfigTerraformMssql
from src.utils import (
    find_obj_name,
    str_to_list_ipaddress,
    validation_ipv4_cidr,
    validation_ipv4_address,
    validation_ipv4_address_list,
    validation_domain,
    validation_domain_list,
    validation_vcpu,
    validation_memory,
    validation_disk,
)
from .vcenter_server import VCenterServer


class MssqlLinux(ConfigBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Config files
        self.terraform = ConfigTerraformMssql(verbose=self.verbose)
        self.ansible = ConfigAnsibleMssql(verbose=self.verbose)

        # Filenames
        self.filename_terraform = "terraform-mssql.tfvars"
        self.filename_ansible = "settings-mssql.yml"

        # Template files
        self.template_folder = Path("templates")
        self.template_terraform = self.template_folder.joinpath(
            f"{self.filename_terraform}.jinja2"
        )
        self.template_ansible = self.template_folder.joinpath(
            f"{self.filename_ansible}.jinja2"
        )

    def prompt(self):
        # Get vCenter host and credentials
        questions = [
            inquirer.Text("vcenter", message="vCenter Server IP or FQDN"),
            inquirer.Text(
                "username",
                message="vCenter username",
                default="administrator@vsphere.local",
            ),
            inquirer.Password("password", message="vCenter password"),
            inquirer.Confirm(
                "allow_insecure_ssl",
                message="Allow insecure SSL connection",
                default=False,
            ),
        ]
        answers = inquirer.prompt(questions, theme=GreenPassion())
        self.terraform.vcenter_server = answers.get("vcenter").strip()
        self.terraform.vcenter_user = answers.get("username").strip()
        self.terraform.vcenter_password = answers.get("password").strip()
        self.terraform.vcenter_insecure_ssl = answers.get("allow_insecure_ssl")

        # Connect to vCenter
        print("Trying to connect and fetch vCenter resources...")
        with VCenterServer(
            host=self.terraform.vcenter_server,
            username=self.terraform.vcenter_user,
            password=self.terraform.vcenter_password,
            allow_insecure_ssl=self.terraform.vcenter_insecure_ssl,
            verbose=self.verbose,
        ) as vc_server:

            # Get datacenters
            vc_datacenters = vc_server.datacenters

            questions = [
                inquirer.List(
                    "vc_datacenter",
                    message="Select datacenter",
                    choices=[x.name for x in vc_datacenters],
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            vc_datacenter = find_obj_name(
                object_list=vc_datacenters, name=answers.get("vc_datacenter")
            )
            self.terraform.vsphere_datacenter = vc_datacenter.name

            # Get cluster
            questions = [
                inquirer.List(
                    "vc_cluster",
                    message="Select cluster",
                    choices=[x.name for x in vc_datacenter.clusters],
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            vc_cluster = find_obj_name(
                object_list=vc_datacenter.clusters,
                name=answers.get("vc_cluster"),
            )
            self.terraform.vsphere_compute_cluster = vc_cluster.name

            # Get datastore
            questions = [
                inquirer.List(
                    "vc_datastore",
                    message="Select datastore",
                    choices=[x.name for x in vc_cluster.datastores],
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            vc_datastore = find_obj_name(
                object_list=vc_cluster.datastores, name=answers.get("vc_datastore")
            )
            self.terraform.vsphere_datastore = vc_datastore.name

            # Get network
            questions = [
                inquirer.List(
                    "vc_network",
                    message="Select network",
                    choices=[x.name for x in vc_cluster.networks],
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            vc_network = find_obj_name(
                object_list=vc_cluster.networks, name=answers.get("vc_network")
            )
            self.terraform.vsphere_network_1_portgroup = vc_network.name

            # Get domain
            questions = [
                inquirer.Text(
                    "vc_network_domain",
                    message=f"Domain name",
                    validate=validation_domain,
                ),
                inquirer.Text(
                    "vc_network_domain_suffixes",
                    message=f"Domain suffix list (comma separated)",
                    validate=validation_domain_list,
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            self.terraform.network_domain_name = answers.get(
                "vc_network_domain"
            ).strip()
            self.terraform.network_dns_suffix = [
                x.strip()
                for x in answers.get("vc_network_domain_suffixes", []).split(",")
            ]

            # Get network ipv4
            questions = [
                inquirer.Text(
                    "vc_network_ipv4_subnet_cidr",
                    message=f"IPv4 network for '{vc_network.name}' (CIDR)",
                    validate=validation_ipv4_cidr,
                ),
                inquirer.Text(
                    "vc_network_ipv4_subnet_gateway",
                    message=f"IPv4 gateway for '{vc_network.name}'",
                    validate=validation_ipv4_address,
                ),
                inquirer.Text(
                    "vc_network_ipv4_dns",
                    message=f"IPv4 DNS (comma separated)",
                    validate=validation_ipv4_address_list,
                ),
                inquirer.Text(
                    "vc_network_ipv4_ips",
                    message=f"IPv4 IP (comma separated)",
                    validate=validation_ipv4_address_list,
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            self.terraform.vsphere_network_1_ipv4_subnet_cidr = IPv4Network(
                answers.get("vc_network_ipv4_subnet_cidr").strip()
            )
            self.terraform.vsphere_network_1_ipv4_gateway = IPv4Address(
                answers.get("vc_network_ipv4_subnet_gateway")
            )
            self.terraform.network_ipv4_dns_servers = str_to_list_ipaddress(
                answers.get("vc_network_ipv4_dns", "")
            )
            self.terraform.vsphere_network_1_ipv4_ips = str_to_list_ipaddress(
                answers.get("vc_network_ipv4_ips", "")
            )

            # Get VM settings
            questions = [
                inquirer.List(
                    "vm_mssql_count",
                    message=f"Number of MSSQL VM",
                    choices=[2, 3, 5, 7, 9],
                    default=2,
                ),
                inquirer.Text(
                    "vm_mssql_vcpu_count",
                    message=f"MSSQL VM vCPU count",
                    validate=validation_vcpu,
                    default=8,
                ),
                inquirer.Text(
                    "vm_mssql_memory_gb",
                    message=f"MSSQL VM memory (GB)",
                    validate=validation_memory,
                    default=32,
                ),
                inquirer.Text(
                    "vm_mssql_data_disk_gb",
                    message=f"MSSQL VM templates disk (GB)",
                    validate=validation_disk,
                    default=100,
                ),
                inquirer.Text(
                    "vm_mssql_log_disk_gb",
                    message=f"MSSQL VM log disk (GB)",
                    validate=validation_disk,
                    default=40,
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            self.terraform.vm_mssql_count = int(answers.get("vm_mssql_count"))
            self.terraform.vm_mssql_vcpu_count = int(answers.get("vm_mssql_vcpu_count"))
            self.terraform.vm_mssql_memory_gb = int(answers.get("vm_mssql_memory_gb"))
            self.terraform.vm_mssql_data_disk_gb = int(
                answers.get("vm_mssql_data_disk_gb")
            )
            self.terraform.vm_mssql_log_disk_gb = int(
                answers.get("vm_mssql_log_disk_gb")
            )

            # Get MSSQL AG settings
            questions = [
                inquirer.List(
                    "mssql_pid",
                    message=f"Choose the MSSQL product edition",
                    choices=["Standard", "Enterprise", "Evaluation"],
                ),
                inquirer.Text(
                    "mssql_ipv4_vip",
                    message=f"Pacemaker IPv4 VIP for MSSQL ({self.terraform.vsphere_network_1_ipv4_subnet_cidr})",
                    validate=validation_ipv4_address,
                ),
                inquirer.Confirm(
                    "mssql_accept_eula",
                    message=f"Do you accept the MSSQL EULA",
                    default=False,
                ),
            ]
            answers = inquirer.prompt(questions, theme=GreenPassion())
            vip_cidr = IPv4Interface(
                f"{answers.get('mssql_ipv4_vip').strip()}/{self.terraform.vsphere_network_1_ipv4_subnet_cidr.prefixlen}"
            )
            self.ansible = ConfigAnsibleMssql(
                mssql_pid=answers.get("mssql_pid"),
                mssql_pcs_cluster_vip_cidr=vip_cidr,
                mssql_accept_eula=answers.get("mssql_accept_eula"),
            )

    def open(self, terraform_file: str, ansible_file: str):
        self.terraform.open(terraform_file)
        self.ansible.open(ansible_file)

    def write(self, terraform_file: str, ansible_file: str):
        self.terraform.write(terraform_file)
        self.ansible.write(ansible_file)

    def validate_vip(self) -> List[str]:
        """This validates if MSSQL VIP is valid."""
        errors = []

        if self.verbose:
            print("Checking if the MSSQL VIP is valid.")

        # Terraform network 1 subnet
        if self.verbose:
            print("Checking network subnet is set... ", end="")
        if not self.terraform.vsphere_network_1_ipv4_subnet_cidr:
            if self.verbose:
                print("ERROR")
            errors.append("Terraform vSphere network 1 subnet is not set.")
        else:
            if self.verbose:
                print("OK")

        # Ansible VIP
        if self.verbose:
            print("Checking MSSQL pacemaker VIP is set... ", end="")
        if not self.ansible.mssql_pcs_cluster_vip_cidr:
            if self.verbose:
                print("ERROR")
            errors.append("MSSQL pacemaker VIp is not set.")
        else:
            if self.verbose:
                print("OK")

        if (
            self.ansible.mssql_pcs_cluster_vip_cidr
            and self.terraform.vsphere_network_1_ipv4_subnet_cidr
        ):
            if self.verbose:
                print("Checking if MSSQL VIP is in the network 1 subnet... ", end="")
            if (
                self.ansible.mssql_pcs_cluster_vip_cidr
                not in self.terraform.vsphere_network_1_ipv4_subnet_cidr
            ):
                if self.verbose:
                    print("ERROR")
                vip = self.ansible.mssql_pcs_cluster_vip_cidr
                subnet = self.terraform.vsphere_network_1_ipv4_subnet_cidr
                errors.append(
                    f"MSSQL pacemaker VIP '{vip}' is not in {subnet}."
                )
            else:
                if self.verbose:
                    print("OK")

            if self.verbose:
                print("Checking if MSSQL VIP conflicts with network 1 IP... ", end="")
            if (
                self.ansible.mssql_pcs_cluster_vip_cidr.ip
                in self.terraform.vsphere_network_1_ipv4_ips
            ):
                if self.verbose:
                    print("ERROR")
                vip = self.ansible.mssql_pcs_cluster_vip_cidr
                errors.append(
                    f"MSSQL pacemaker VIP '{vip}' conflicts with an address in the network 1 IP list."
                )
            else:
                if self.verbose:
                    print("OK")

        return errors

    def validate(self, verbose: bool = True) -> List[str]:
        errors = []
        try:
            errors.extend(self.terraform.validate())
            errors.extend(self.ansible.validate())
            errors.extend(self.validate_vip())
        except ValueError as e:
            print(e)

        return errors
