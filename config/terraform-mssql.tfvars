#
# Resource Pool
#
resource_pool = "mssql-linux"

#
# MSSQL Linux VM
#
mssql_linux_vm_prefix = "mssql-linux"
mssql_linux_vm_count = 4
mssql_linux_vm = {
    cpu = 16
    memory_gb = 64
    os_disk_gb = 100
    data_disk_gb = 250
}
