#
# Resource Pool
#
resource_pool = "mssql-linux"

#
# MSSQL Linux VM
#
mssql_linux_vm_prefix = "mssql-linux"
mssql_linux_vm_count = 3
mssql_linux_vm = {
    cpu = 8
    memory_gb = 32
    os_disk_gb = 60
    data_disk_gb = 100
}
