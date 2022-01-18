#!/bin/bash 

ANSIBLE_INVENTORY="../config/inventory.yml"
ANSIBLE_MSSQL="../config/settings.yml"
ANSIBLE_TEMPLATE="../config/settings-template.yml"


if [ ! -f "${ANSIBLE_INVENTORY}" ]; then
    echo "ERROR: The file ${ANSIBLE_INVENTORY} is missing."
    exit 1
fi

if [ ! -f "${ANSIBLE_MSSQL}" ]; then
    echo "ERROR: The file ${ANSIBLE_MSSQL} is missing."
    exit 1
fi

if [ ! -f "${ANSIBLE_TEMPLATE}" ]; then
    echo "ERROR: The file ${ANSIBLE_TEMPLATE} is missing."
    exit 1
fi

# Configure the systems
ansible-playbook -i "${ANSIBLE_INVENTORY}" \
                 -i "${ANSIBLE_MSSQL}" \
                 -i "${ANSIBLE_TEMPLATE}" \
                 all.yml
