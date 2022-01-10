#
# vSphere vCenter Server
#
variable vcenter_server {
    description = "vCenter Server hostname or IP"
    type = string
}

variable vcenter_user {
    description = "vCenter Server username"
    type = string
}

variable vcenter_password {
    description = "vCenter Server password"
    type = string
}

variable vcenter_insecure_ssl {
    description = "Allow insecure connection to the vCenter server (unverified SSL certificate)"
    type = bool
    default = false
}

#
# vSphere Cluster
#
variable vsphere_cluster {
  type = object({
    # vSphere Datacenter
    vs_dc = string

    # vSphere Cluster in the Datacenter
    vs_cls = string

    # vSphere Resource Pool
    vs_rp = string

    # vSphere Distributed Virtual Switch
    vs_dvs = string

    # vSphere Distributed Portgroup
    vs_dvs_pg_1 = string

    # Portgroup 1 IPv4 subnet in CIDR notation (e.g. 10.0.0.0/24)
    vs_dvs_pg_1_ipv4_subnet = string

    # Portgroup 1 IPv4 addresses
    vs_dvs_pg_1_ipv4_ips = list(string)

    # Portgroup 1 IPv4 gateway address
    vs_dvs_pg_1_ipv4_gw = string

    # vSphere Distributed Portgroup
    vs_dvs_pg_2 = string

    # Portgroup 2 IPv4 subnet in CIDR notation (e.g. 10.0.0.0/24)
    vs_dvs_pg_2_ipv4_subnet = string

    # Portgroup 2 IPv4 addresses
    vs_dvs_pg_2_ipv4_ips = list(string)

    # Portgroup 2 IPv4 gateway address
    vs_dvs_pg_2_ipv4_gw = string

    # vSphere vSAN datastore
    vs_ds = string

    # vSphere vSAN Storage Policy
    vs_ds_sp = string

    # Virtual machine domain name
    vs_vm_domain = string

    # Virtual Machine DNS servers
    vs_vm_dns = list(string)

    # Virtual Machine DNS suffixes
    vs_vm_dns_suffix = list(string)
  })
}

#
# Template
#
variable template_library_name {
  type = string
}

variable template_ova {
  type = string
}

variable template_name {
  type = string
}

variable template_description {
  type = string
}

variable template_boot {
  type = string
  default = "efi"
}

#
# Resource Pool
#
variable "resource_pool" {
  type = string
}


#
# MSSQL Linux VM
#

variable mssql_linux_vm_count {
    type = number
    default = 3
}

variable mssql_linux_vm_prefix {
    type = string
    default = "linux"
}

variable mssql_linux_vm {
    type = object({
        cpu = number
        memory_gb = number
        os_disk_gb = number
        data_disk_gb = number
    })
}
