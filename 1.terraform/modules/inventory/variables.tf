variable "input" {
  description = "A map of inventory group names to IP addresses."
}

variable "output_folder" {
  type = string
  description = "The path to use when saving the rendered inventory file."
}