#! /bin/bash

TERRAFORM_DIR="terraform"

# Terraform
echo "Destroying Virtual Machines"
pushd "$TERRAFORM_DIR" > /dev/null
  ./destroy.sh
popd > /dev/null

echo "Cleanup old certificates"
pushd config > /dev/null
  rm -f *.cer
popd > /dev/null
