#! /bin/bash

DIR_CONFIG="config"
DIR_TERRAFORM="terraform"
DIR_ANSIBLE="ansible"

TERRAFORM_TFVARS_HOME="$(realpath ~/terraform-mssql.tfvars)"
TERRAFORM_TFVARS_CONFIG="terraform-mssql.tfvars"
TERRAFORM_UBUNTU_20_04_HW14="terraform-ubuntu-20.04-hw14.tfvars"

ANSIBLE_MSSQL_HOME="$(realpath ~/settings-mssql.yml)"
ANSIBLE_MSSQL_CONFIG="settings-mssql.yml"
ANSIBLE_UBUNTU_20_04="settings-ubuntu-20.04.yml"

# Configuration
echo "Setting configurations"
pushd "${DIR_CONFIG}" > /dev/null

  echo "Setting terraform variables..."
  ln -f -s "${TERRAFORM_UBUNTU_20_04_HW14}" "terraform-template.tfvars"
  if [ -f "${TERRAFORM_TFVARS_HOME}" ]; then 
    echo "Using settings in the home folder"
    ln -f -s "${TERRAFORM_TFVARS_HOME}" "terraform.tfvars"
  else
    echo "Using settings in the config folder"
    ln -f -s "${TERRAFORM_TFVARS_CONFIG}" "terraform.tfvars"
  fi

  echo "Setting ansible variables..."
  ln -f -s "${ANSIBLE_UBUNTU_20_04}" "settings-template.yml"
  if [ -f "${ANSIBLE_MSSQL_HOME}" ]; then
    echo "Using settings in home folder"
    ln -f -s "${ANSIBLE_MSSQL_HOME}" "settings.yml"
  else
    echo "Using settings in the config folder"
    ln -f -s "${ANSIBLE_MSSQL_CONFIG}" "settings.yml"
  fi
popd > /dev/null

# Validation
pushd "lib/mssql-linux-config" > /dev/null

pipenv run python main.py validate \
-t /opt/automation/automation-mssql-linux/config/terraform.tfvars \
-a /opt/automation/automation-mssql-linux/config/settings.yml \
-v

ret=$?
if [ $ret -ne 0 ]; then
  exit $ret
fi

popd > /dev/null

# Terraform
echo "Running terraform plan"
pushd "${DIR_TERRAFORM}" > /dev/null
  ./plan.sh
  [ $? -eq 0 ]  || exit 1
popd > /dev/null
