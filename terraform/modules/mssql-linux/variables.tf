#
# vSphere Variables
# -----------------------------------------------------------------------------
# Datacenter
variable "vsphere_datacenter" {
  type = string
}

# Cluster
variable "vsphere_compute_cluster" {
  type = string
}

# Resource Pool
variable "vsphere_resource_pool" {
  type = string
}

# Network 1 Distributed Portgroup
variable "vsphere_network_1_portgroup" {
  type = string
}

# Network 1 IPv4 Subnet (CIDR)
variable "vsphere_network_1_ipv4_subnet_cidr" {
  type = string
}

# Network 1 IPv4 IP List
variable "vsphere_network_1_ipv4_ips" {
  type = list(string)
}

# Network 1 IPv4 IP List
variable "vsphere_network_1_ipv4_gateway" {
  type = string
}

# Datastore
variable "vsphere_datastore" {
  type = string
}

variable "vsphere_folder_vm" {
  type = string
  default = "mssql-linux"
}

#
# Network
# -----------------------------------------------------------------------------
# Domain Name
variable "network_domain_name" {
  type = string
}

# Domain Name
variable "network_ipv4_dns_servers" {
  type    = list(string)
  default = ["8.8.8.8", "8.8.4.4"]
}

# Domain Name
variable "network_dns_suffix" {
  type    = list(string)
  default = []
}

#
# Template
# -----------------------------------------------------------------------------
variable template {
  type = map
}

variable template_boot {
  type = string
}

#
# VM MSSQL
# -----------------------------------------------------------------------------
variable "vm_mssql_prefix" {
  type = string
  default = "mssql-linux"
}

variable "vm_mssql_count" {
  type = number
  default = 3
}

variable "vm_mssql" {
  type = object({
    cpu          = number
    memory_gb    = number
    os_disk_gb   = number
    data_disk_gb = number
    log_disk_gb  = number
  })
}

variable "vm_mssql_anti_affinity" {
  type = bool
  default = true
}
