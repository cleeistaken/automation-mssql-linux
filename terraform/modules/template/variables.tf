#
# vSphere
# -----------------------------------------------------------------------------
# Datacenter
variable "vsphere_datacenter" {
  type = string
}

# Datastore
variable "vsphere_datastore" {
  type = string
}

#
# Content Library
# -----------------------------------------------------------------------------
variable content_library_name {
  type    = string
  default = "Content Library Test"
}

variable content_library_description {
  type    = string
  default = "A new source of content"
}

#
# Content Library Template
# -----------------------------------------------------------------------------
variable content_library_item_name {
  type = string
}

variable content_library_item_description {
  type = string
}

variable content_library_item_url {
  type = string
}
