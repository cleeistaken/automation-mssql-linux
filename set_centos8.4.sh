#! /bin/bash

pushd config/
  echo "Setting Centos 8.4"
  ln -f -s settings-template.yml.centos8.4 settings-template.yml
  ln -f -s terraform.tfvars.centos8.4 terraform.tfvars
popd
