#! /bin/bash

pushd config/
  echo "Setting Ubuntu 20.04"
  ln -f -s settings-template.yml.ubuntu20.04 settings-template.yml
  ln -f -s terraform.tfvars.ubuntu20.04_hw14 terraform.tfvars
popd
