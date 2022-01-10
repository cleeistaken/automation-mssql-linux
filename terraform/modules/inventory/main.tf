resource "local_file" "inventory" {
  content  = templatefile("${path.module}/inventory.yml.tpl", { vms = var.input, vsphere_server = var.vsphere_server, user = var.user, password = var.password, allow_unverified_ssl = var.allow_unverified_ssl })
  filename = "${var.output_folder}/inventory.yml"
  file_permission = "644"
}

