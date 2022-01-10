#
# Content Library
#
data "vsphere_datacenter" "vs_dc" {
  name = var.vsphere_cluster.vs_dc
}

data "vsphere_datastore" "vs_ds" {
  name = var.vsphere_cluster.vs_ds
  datacenter_id = data.vsphere_datacenter.vs_dc.id
}

resource "vsphere_content_library" "content_library" {
  name            = var.content_library_name
  description     = var.content_library_description
  storage_backing = [data.vsphere_datastore.vs_ds.id]
}

resource "vsphere_content_library_item" "content_library_item" {
  name        = var.content_library_item_name
  description = var.content_library_item_description
  library_id  = vsphere_content_library.content_library.id
  file_url = var.content_library_item_url
}
