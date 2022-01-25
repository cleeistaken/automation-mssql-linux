# This file contains all the parameters required by Terraform
# in order to connect and identify the resources to use in the
# target vSphere cluster.

#
# vCenter Server Configuration
#
# vCenter Hostname or IP
vcenter_server = "vc.vmware.home"

# Username
vcenter_user = "administrator@vsphere.local"

# Password
vcenter_password = "VMware1!"

# Allow unverified SSL connection
vcenter_insecure_ssl = true

#
# vSphere Configuration
#
# vSphere Datacenter.
# This resource must exist.
vsphere_datacenter = "Datacenter"

# vSphere Cluster in the Datacenter.
# This resource must exist.
vsphere_compute_cluster = "Cluster"

# vSphere VM Folder containing the created VM.
# This resource must not exist and will be created by Terraform. <---
vsphere_folder_vm = "mssql"

# vSphere Resource Pool where the VM will be created.
# This resource must not exist and will be created by Terraform. <---
vsphere_resource_pool = "mssql"

# vSphere Distributed Switch with the target portgroup.
# This resource must exist.
vsphere_distributed_switch = "DSwitch"

# vSphere Distributed Switch PortGroup.
# This resource must exist.
vsphere_network_1_portgroup = "DPortGroup"

# Subnet for the PortGroup.
# This must be configured in CIDR format "<network>/<mask>" (e.g. "10.0.0.0/8")
vsphere_network_1_ipv4_subnet_cidr = "10.0.0.0/8"

# List of IP addresses that will be used for the created VM.
# There must be as many IP as the requested number of MSSQL VM nodes (see 'vm_mssql_count').
# The IP addresses must not be in use.
vsphere_network_1_ipv4_ips = ["10.0.1.1", "10.0.1.2", "10.0.1.3", "10.0.1.4", "10.0.1.5"]

# Address of the gateway for the PortGroup subnet.
vsphere_network_1_ipv4_gateway = "10.0.0.1"

# The target Datastore for the created VM.
# This resource must exist and have sufficient available capacity.
vsphere_datastore = "vsanDatastore"

# Datastore Storage Policy
# This resource must exist.
vsphere_storage_policy = "vSAN Default Storage Policy"

#
# Network
#
# Domain that will be appended to the hostname
network_domain_name = "vmware.home"

# DNS servers that will be configured on the created VM
network_ipv4_dns_servers = ["8.8.8.8", "8.8.4.4"]

# DNS suffix search list
network_dns_suffix = []

#
# VM MSSQL
#
# The prefix for the VM create in the
vm_mssql_prefix = "mssql-linux"

# The number of MSSQL VM to create.
# Currently this project only support nodes counts of 3 or 5. The SQL Server Linux AG
# replica are configured with the synchronized commit option.
vm_mssql_count = 3

# The VM hardware configuration
vm_mssql = {
    cpu = 8            # Number of vCPU
    memory_gb = 32     # Amount of RAM in GB
    os_disk_gb = 60    # Size of the OS disk
    data_disk_gb = 100 # Size of the disk where the MSSQL data will reside
}
