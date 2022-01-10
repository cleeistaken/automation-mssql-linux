#! /bin/bash

echo "Cleaning up Terraform state files"
rm -f terraform.tfstate  
rm -f terraform.tfstate.backup
