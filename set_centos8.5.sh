#! /bin/bash

pushd config/
  echo "Setting Centos 8.5"
  ln -f -s settings-template.yml.centos8.5 settings-template.yml
  ln -f -s terraform.tfvars.centos8.5 terraform.tfvars
popd
