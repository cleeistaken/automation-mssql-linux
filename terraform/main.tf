#
# vSphere Provider
#
provider "vsphere" {
  vsphere_server = var.vcenter_server
  user = var.vcenter_user
  password = var.vcenter_password
  allow_unverified_ssl = var.vcenter_insecure_ssl
}

#
# Get Local IP
#
data "external" "local_ip" {
  program = ["./get-ip.sh"]
}

#
# Content Library
#
module "template" {
  source = "./modules/template"

  # vSphere Cluster
  vsphere_datacenter = var.vsphere_datacenter
  vsphere_datastore = var.vsphere_datastore

  # Template
  content_library_name = var.template_library_name
  content_library_item_url = format("http://%s/templates/%s", data.external.local_ip.result.ip, var.template_ova)
  content_library_item_name = var.template_name
  content_library_item_description = var.template_description
}

#
# MSSQL VM
#
module "mssql-linux" {
  source = "./modules/mssql-linux"

  # vSphere
  vsphere_datacenter = var.vsphere_datacenter
  vsphere_compute_cluster = var.vsphere_compute_cluster
  vsphere_resource_pool = var.vsphere_resource_pool
  vsphere_distributed_switch = var.vsphere_distributed_switch
  vsphere_network_1_portgroup = var.vsphere_network_1_portgroup
  vsphere_network_1_ipv4_subnet_cidr = var.vsphere_network_1_ipv4_subnet_cidr
  vsphere_network_1_ipv4_ips = var.vsphere_network_1_ipv4_ips
  vsphere_network_1_ipv4_gateway = var.vsphere_network_1_ipv4_gateway
  vsphere_datastore = var.vsphere_datastore
  vsphere_storage_policy = var.vsphere_storage_policy

  # Network
  network_domain_name = var.network_domain_name
  network_ipv4_dns_servers = var.network_ipv4_dns_servers
  network_dns_suffix = var.network_dns_suffix

  # Template
  template = module.template.content_library_item
  template_boot = var.template_boot

  # VM MSSQL
  vm_mssql_prefix = var.vm_mssql_prefix
  vm_mssql_count = var.vm_mssql_count
  vm_mssql = var.vm_mssql
}
