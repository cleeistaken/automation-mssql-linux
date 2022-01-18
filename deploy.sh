#! /bin/bash

DIR_CONFIG="config"
DIR_TERRAFORM="terraform"
DIR_ANSIBLE="ansible"

# Template Variables
# For now we will only use Ubuntu 20.04 with HW14
TERRAFORM_TFVARS_HOME="$(realpath ~/terraform-mssql.tfvars)"
TERRAFORM_TFVARS_CONFIG="terraform-mssql.tfvars"
TERRAFORM_UBUNTU_20_04_HW14="terraform-ubuntu-20.04-hw14.tfvars"
ANSIBLE_UBUNTU_20_04="settings-ubuntu-20.04.yml"

echo "$TERRAFORM_TFVARS_HOME"

# Configuration
echo "Setting configurations"
pushd "${DIR_CONFIG}" > /dev/null

  echo "Setting terraform variables..."
  if [ -f "${TERRAFORM_TFVARS_HOME}" ]; then 
    echo "Using settings in the home folder"
    ln -f -s "${TERRAFORM_TFVARS_HOME}" "terraform.tfvars"
  else
    echo "Using settings in the config folder"
    ln -f -s "${TERRAFORM_TFVARS_CONFIG}" "terraform.tfvars"
  fi
  ln -f -s "${TERRAFORM_UBUNTU_20_04_HW14}" "terraform-template.tfvars"

  echo "Setting ansible variables..."
  ln -f -s "${ANSIBLE_UBUNTU_20_04}" "settings.yml"
popd > /dev/null

# Terraform
echo "Deploying Virtual Machines"
pushd "${DIR_TERRAFORM}" > /dev/null
  ./deploy.sh
  [ $? -eq 0 ]  || exit 1
popd > /dev/null

# Ansible VM Setup
echo "Configuring VM"
pushd "${DIR_ANSIBLE}" > /dev/null
  #./deploy.sh
  #[ $? -eq 0 ]  || exit 1
popd > /dev/null

