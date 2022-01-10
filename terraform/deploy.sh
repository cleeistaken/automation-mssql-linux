#! /bin/bash

terraform init

terraform apply \
-auto-approve \
--var-file=../../config/terraform.tfvars.mssql \
--var-file=../config/terraform.tfvars \
--var-file=../config/terraform-mssql.tfvars
