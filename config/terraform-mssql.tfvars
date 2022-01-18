#
# vCenter Server Configuration
#
vcenter_server = "vc.vmware.home"
vcenter_user = "administrator@vsphere.local"
vcenter_password = "VMware1!"
vcenter_insecure_ssl = true

#
# vSphere Configuration
#
vsphere_datacenter = "Datacenter"
vsphere_compute_cluster = "Cluster"
vsphere_resource_pool = "Resource Pool"
vsphere_distributed_switch = "DSwitch"
vsphere_network_1_portgroup = "DPortGroup"
vsphere_network_1_ipv4_subnet_cidr = "10.0.0.0/8"
vsphere_network_1_ipv4_ips = ["10.0.1.1", "10.0.1.2", "10.0.1.3", "10.0.1.4", "10.0.1.5"]
vsphere_network_1_ipv4_gateway = "10.0.0.1"
vsphere_datastore = "vsanDatatstore"
vsphere_storage_policy = "vSAN Default Storage Policy"

#
# Network
#
network_domain_name = "vmware.home"
network_ipv4_dns_servers = ["8.8.8.8", "8.8.4.4"]
network_dns_suffix = []

#
# VM MSSQL
#
mssql_linux_vm_prefix = "mssql-linux"
mssql_linux_vm_count = 3
mssql_linux_vm = {
    cpu = 8
    memory_gb = 32
    os_disk_gb = 60
    data_disk_gb = 100
}
