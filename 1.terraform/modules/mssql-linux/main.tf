#
# Cluster
#
data "vsphere_datacenter" "vs_dc" {
  name = var.vsphere_cluster.vs_dc
}

data "vsphere_compute_cluster" "vs_cc" {
  name          = var.vsphere_cluster.vs_cls
  datacenter_id = data.vsphere_datacenter.vs_dc.id
}

resource "vsphere_resource_pool" "vs_rp" {
  name                    = var.resource_pool
  parent_resource_pool_id = data.vsphere_compute_cluster.vs_cc.resource_pool_id
}

data "vsphere_datastore" "vs_ds" {
  name          = var.vsphere_cluster.vs_ds
  datacenter_id = data.vsphere_datacenter.vs_dc.id
}

data "vsphere_storage_policy" "vs_ds_policy" {
  name = var.vsphere_cluster.vs_ds_sp
}

data "vsphere_distributed_virtual_switch" "vs_dvs" {
  name          = var.vsphere_cluster.vs_dvs
  datacenter_id = data.vsphere_datacenter.vs_dc.id
}

data "vsphere_network" "vs_dvs_pg_public" {
  name                            = var.vsphere_cluster.vs_dvs_pg_1
  datacenter_id                   = data.vsphere_datacenter.vs_dc.id
  distributed_virtual_switch_uuid = data.vsphere_distributed_virtual_switch.vs_dvs.id
}

data "vsphere_network" "vs_dvs_pg_private" {
  name                            = var.vsphere_cluster.vs_dvs_pg_2
  datacenter_id                   = data.vsphere_datacenter.vs_dc.id
  distributed_virtual_switch_uuid = data.vsphere_distributed_virtual_switch.vs_dvs.id
}

#
# MSSQL Linux
#
resource "vsphere_virtual_machine" "mssql_linux_vm" {
  count = var.mssql_linux_vm_count
  name  = format("%s-%02d", var.mssql_linux_vm_prefix, count.index + 1)

  # VM template
  #guest_id = data.vsphere_virtual_machine.vs_vm_template.guest_id

  # Template boot mode (efi or bios)
  firmware = var.template_boot

  # Resource pool for created VM
  resource_pool_id = vsphere_resource_pool.vs_rp.id

  # Datastore and Storage Policy
  datastore_id      = data.vsphere_datastore.vs_ds.id
  storage_policy_id = data.vsphere_storage_policy.vs_ds_policy.id

  num_cpus = var.mssql_linux_vm.cpu
  memory   = var.mssql_linux_vm.memory_gb * 1024

  network_interface {
    network_id  = data.vsphere_network.vs_dvs_pg_public.id
    ovf_mapping = "eth0"
  }

  scsi_controller_count = 2

  disk {
    label       = format("%s-%02d-os-disk0", var.mssql_linux_vm_prefix, count.index + 1)
    size        = var.mssql_linux_vm.os_disk_gb
    unit_number = 0
  }

  # scsi0:0-14 are unit numbers 0-14
  # scsi1:0-14 are unit numbers 15-29
  # scsi2:0-14 are unit numbers 30-44
  # scsi3:0-14 are unit numbers 45-59
  dynamic "disk" {
    for_each = range(0, 1)

    content {
      label             = format("%s-%02d-%s-disk%d", var.mssql_linux_vm_prefix, (count.index + 1), "data", (disk.value + 1))
      size              = var.mssql_linux_vm.data_disk_gb
      storage_policy_id = data.vsphere_storage_policy.vs_ds_policy.id
      unit_number       = 15 + ((disk.value % 3) * 14) + disk.value
    }
  }

  clone {
    template_uuid = var.template.id

    customize {
      linux_options {
        host_name = format("%s-%02d", var.mssql_linux_vm_prefix, count.index + 1)
        domain    = var.vsphere_cluster.vs_vm_domain
      }

      network_interface {
        ipv4_address = var.vsphere_cluster.vs_dvs_pg_1_ipv4_ips[count.index]
        ipv4_netmask = regex("/([0-9]{1,2})$", var.vsphere_cluster.vs_dvs_pg_1_ipv4_subnet)[0]
      }

      ipv4_gateway    = var.vsphere_cluster.vs_dvs_pg_1_ipv4_gw
      dns_server_list = var.vsphere_cluster.vs_vm_dns
      dns_suffix_list = var.vsphere_cluster.vs_vm_dns_suffix

    }
  }
}
