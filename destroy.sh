#! /bin/bash

TERRAFORM_DIR="terraform"

# Terraform
echo "Destroying Virtual Machines"
pushd "$TERRAFORM_DIR"
  ./destroy.sh
popd
