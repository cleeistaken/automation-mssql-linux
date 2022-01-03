output "mssql_linux" {
  value = module.mssql-linux
  sensitive = true
}


#
# Inventory File
#
module "inventory" {
  source  = "./modules/inventory"
  input = module.mssql-linux
  output_folder = "../config"
}
