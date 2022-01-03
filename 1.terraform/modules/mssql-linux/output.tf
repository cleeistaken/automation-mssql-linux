output "mssql_linux_env" {
  value = {
    "mssql_linux" = vsphere_virtual_machine.mssql_linux_vm
  }
}