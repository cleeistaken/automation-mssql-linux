#!/bin/bash 

# Configure the systems
ansible-playbook -i ../config/settings-mssql.yml \
                 -i ../config/settings-template.yml \
                 -i ../config/inventory.yml \
                 --extra-vars "local_repo=false" \
                 all.yml
