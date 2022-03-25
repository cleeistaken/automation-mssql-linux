#!/bin/bash
pushd "lib/mssql-linux-config" > /dev/null
pipenv run python main.py prompt \
-t /opt/automation/automation-mssql-linux/config/settings-mssql.yml \
-a /opt/automation/automation-mssql-linux/config/terraform-mssql.tfvars \
-v
popd > /dev/null