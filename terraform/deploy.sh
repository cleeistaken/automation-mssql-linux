#! /bin/bash

TERRAFORM_MSSQL="../config/terraform-mssql.tfvars"
TERRAFORM_TEMPLATE="../config/terraform-template.tfvars"

if [ ! -f "${TERRAFORM_MSSQL}" ]; then
    echo "ERROR: The file ${TERRAFORM_MSSQL} is missing."
    exit 1
fi

if [ ! -f "${TERRAFORM_TEMPLATE}" ]; then
    echo "ERROR: The file ${TERRAFORM_TEMPLATE} is missing."
    exit 1
fi

# Make sure terraform is initialized
terraform init

# Invoke terraform to build the environment
terraform apply \
-auto-approve \
--var-file=../config/terraform-mssql.tfvars \
--var-file=../config/terraform-template.tfvars
