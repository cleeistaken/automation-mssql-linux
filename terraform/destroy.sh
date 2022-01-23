#! /bin/bash

TERRAFORM_MSSQL="../config/terraform.tfvars"
TERRAFORM_TEMPLATE="../config/terraform-template.tfvars"
TERRAFORM_TFPLAN="tfplan"

if [ ! -f "${TERRAFORM_MSSQL}" ]; then
    echo "ERROR: The file ${TERRAFORM_MSSQL} is missing."
    exit 1
fi

if [ ! -f "${TERRAFORM_TEMPLATE}" ]; then
    echo "ERROR: The file ${TERRAFORM_TEMPLATE} is missing."
    exit 1
fi

terraform destroy \
-auto-approve \
--var-file="${TERRAFORM_MSSQL}" \
--var-file="${TERRAFORM_TEMPLATE}"

if [ -f "${TERRAFORM_TFPLAN}" ]; then
    echo "Removing tfplan file"
    rm -f "${TERRAFORM_TFPLAN}"
fi
