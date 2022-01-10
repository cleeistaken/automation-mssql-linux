variable "input" {
  description = "A map of inventory group names to IP addresses."
}

variable "vsphere_server" {
  type = string
}

variable "user" {
  type = string
}

variable "password" {
  type = string
}

variable "allow_unverified_ssl" {
  type = bool
}

variable "output_folder" {
  type = string
  description = "The path to use when saving the rendered inventory file."
}