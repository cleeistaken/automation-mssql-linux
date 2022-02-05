#
# Cluster
#
data "vsphere_datacenter" "vsphere_datacenter_1" {
  name = var.vsphere_datacenter
}

resource "vsphere_folder" "vsphere_folder_1" {
  path          = var.vsphere_folder_vm
  type          = "vm"
  datacenter_id = data.vsphere_datacenter.vsphere_datacenter_1.id
}

data "vsphere_compute_cluster" "vsphere_compute_cluster_1" {
  name          = var.vsphere_compute_cluster
  datacenter_id = data.vsphere_datacenter.vsphere_datacenter_1.id
}

resource "vsphere_resource_pool" "vsphere_resource_pool_1" {
  name                    = var.vsphere_resource_pool
  parent_resource_pool_id = data.vsphere_compute_cluster.vsphere_compute_cluster_1.resource_pool_id
}

data "vsphere_datastore" "vsphere_datastore_1" {
  name          = var.vsphere_datastore
  datacenter_id = data.vsphere_datacenter.vsphere_datacenter_1.id
}

data "vsphere_distributed_virtual_switch" "vsphere_distributed_virtual_switch_1" {
  name          = var.vsphere_distributed_switch
  datacenter_id = data.vsphere_datacenter.vsphere_datacenter_1.id
}

data "vsphere_network" "vsphere_network_1" {
  name                            = var.vsphere_network_1_portgroup
  datacenter_id                   = data.vsphere_datacenter.vsphere_datacenter_1.id
  distributed_virtual_switch_uuid = data.vsphere_distributed_virtual_switch.vsphere_distributed_virtual_switch_1.id
}

locals {
  disks = tolist([var.vm_mssql.data_disk_gb, var.vm_mssql.log_disk_gb])
}


#
# MSSQL Linux
#
resource "vsphere_virtual_machine" "mssql_linux_vm" {
  count = var.vm_mssql_count
  name  = format("%s-%02d", var.vm_mssql_prefix, count.index + 1)

  # VM template
  #guest_id = data.vsphere_virtual_machine.vs_vm_template.guest_id

  # Template boot mode (efi or bios)
  firmware = var.template_boot

  # VM Folder
  folder = vsphere_folder.vsphere_folder_1.path

  # Resource pool for created VM
  resource_pool_id = vsphere_resource_pool.vsphere_resource_pool_1.id

  # Datastore and Storage Policy
  datastore_id      = data.vsphere_datastore.vsphere_datastore_1.id

  num_cpus = var.vm_mssql.cpu
  memory   = var.vm_mssql.memory_gb * 1024

  network_interface {
    network_id  = data.vsphere_network.vsphere_network_1.id
    ovf_mapping = "eth0"
  }

  scsi_controller_count = max(1, min(3, length(local.disks)))

  disk {
    label       = format("%s-%02d-os-disk0", var.vm_mssql_prefix, count.index + 1)
    size        = var.vm_mssql.os_disk_gb
    unit_number = 0
  }

  # scsi0:0-14 are unit numbers 0-14
  # scsi1:0-14 are unit numbers 15-29
  # scsi2:0-14 are unit numbers 30-44
  # scsi3:0-14 are unit numbers 45-59
   dynamic "disk" {
    for_each = range(0, length(local.disks))

    content {
      label             = format("%s-%02d-%s-disk%d", var.vm_mssql_prefix, (count.index + 1), "data", (disk.value + 1))
      size              = local.disks[disk.value]
      unit_number       = 15 + ((disk.value % 3) * 14) + disk.value
    }
  }

  clone {
    template_uuid = var.template.id

    customize {
      linux_options {
        host_name = format("%s-%02d", var.vm_mssql_prefix, count.index + 1)
        domain    = var.network_domain_name
      }

      network_interface {
        ipv4_address = var.vsphere_network_1_ipv4_ips[count.index]
        ipv4_netmask = regex("/([0-9]{1,2})$", var.vsphere_network_1_ipv4_subnet_cidr)[0]
      }

      ipv4_gateway    = var.vsphere_network_1_ipv4_gateway
      dns_server_list = var.network_ipv4_dns_servers
      dns_suffix_list = var.network_dns_suffix
    }
  }
}

# Anti-affinity rule
resource "vsphere_compute_cluster_vm_anti_affinity_rule" "mssql_anti_affinity_rule" {
  count               = var.vm_mssql_count > 0 ? 1 : 0
  name                = format("%s-anti-affinity-rule", var.vm_mssql_prefix)
  compute_cluster_id  = data.vsphere_compute_cluster.vsphere_compute_cluster_1.id
  virtual_machine_ids = vsphere_virtual_machine.mssql_linux_vm.*.id
}
