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

# Make sure terraform is initialized
echo "Initializing Terraform..."
terraform init

if [ -f "${TERRAFORM_TFPLAN}" ]; then
    # Invoke terraform to build the environment
    echo "Applying Terraform using tfplan"
    terraform apply "${TERRAFORM_TFPLAN}" 
else
    # Invoke terraform to build the environment
    echo "Applying Terraform"
    terraform apply \
    -auto-approve \
    --var-file="${TERRAFORM_MSSQL}" \
    --var-file="${TERRAFORM_TEMPLATE}"
fi
