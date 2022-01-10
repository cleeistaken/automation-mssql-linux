#! /bin/bash

terraform destroy \
-auto-approve \
--var-file=../../config/terraform.tfvars \
--var-file=../config/terraform.tfvars \
--var-file=../config/terraform-mssql.tfvars
