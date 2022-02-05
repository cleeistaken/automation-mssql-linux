#
# vSphere vCenter Server
#
variable vcenter_server {
  description = "vCenter Server hostname or IP"
  type        = string
}

variable vcenter_user {
  description = "vCenter Server username"
  type        = string
}

variable vcenter_password {
  description = "vCenter Server password"
  type        = string
}

variable vcenter_insecure_ssl {
  description = "Allow insecure connection to the vCenter server (unverified SSL certificate)"
  type        = bool
  default     = false
}

#
# Content Library and Template
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
  type    = string
  default = "efi"
}

#
# vSphere
#

# Datacenter
variable "vsphere_datacenter" {
  description = "vSphere Datacenter (This resource must exist)"
  type        = string
  default     = "Datacenter"
}

# Cluster
variable "vsphere_compute_cluster" {
  description = "vSphere Cluster (This resource must exist)"
  type        = string
  default     = "New Cluster"
}

# VM Folder
variable "vsphere_folder_vm" {
  description = "vSphere VM folder (This resource will be created <---)"
  type = string
  default = "mssql-linux"
}

# Resource Pool
variable "vsphere_resource_pool" {
  description = "vSphere Resource Pool (This resource will be created <---)"
  type        = string
  default     = "New Resource Pool"
}

# Network 1 Distributed vSwitch
variable "vsphere_distributed_switch" {
  description = "vSphere Distributed Switch (This resource must exist)"
  type        = string
  default     = "DSwitch"
}

# Network 1 Distributed Portgroup
variable "vsphere_network_1_portgroup" {
  description = "vSphere Distributed Switch Portgroup 1 (This resource must exist)"
  type        = string
  default     = "DPortGroup"
}

# Network 1 IPv4 Subnet (CIDR)
variable "vsphere_network_1_ipv4_subnet_cidr" {
  description = "vSphere Distributed Switch Portgroup 1 IPv4 Subnet (CIDR format)"
  type        = string
}

# Network 1 IPv4 IP List
variable "vsphere_network_1_ipv4_ips" {
  description = "vSphere Distributed Switch Portgroup 1 IPv4 IP list"
  type        = list(string)
}

# Network 1 IPv4 IP Gateway
variable "vsphere_network_1_ipv4_gateway" {
  description = "vSphere Distributed Switch Portgroup 1 IPv4 Gateway"
  type        = string
}

# Datastore
variable "vsphere_datastore" {
  description = "vSphere Datastore (This resource must exist)"
  type        = string
  default     = "vsanDatastore"
}

# Domain Name
variable "network_domain_name" {
  description = "Domain name to be appended to the hostname"
  type        = string
}

# DNS Servers
variable "network_ipv4_dns_servers" {
  description = "List of DNS servers"
  type        = list(string)
  default     = ["8.8.8.8", "8.8.4.4"]
}

# DNS Suffixes
variable "network_dns_suffix" {
  description = "List of DNS suffixes"
  type        = list(string)
  default     = []
}

#
# VM MSSQL
#
variable "vm_mssql_prefix" {
  description = "VM prefix"
  type        = string
  default     = "mssql"
}

variable "vm_mssql_count" {
  description = "Number of MSSQL VM"
  type        = number
  default     = 3
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
