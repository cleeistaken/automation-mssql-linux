resource "local_file" "inventory" {
  content  = templatefile("${path.module}/inventory.yml.tpl", { vms = var.input })
  filename = "${var.output_folder}/inventory.yml"
  file_permission = "644"
}

