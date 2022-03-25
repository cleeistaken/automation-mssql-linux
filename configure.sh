#!/bin/bash
pushd "lib/mssql-linux-config" > /dev/null
pipenv run python main.py prompt \
-t /opt/automation/automation-mssql-linux/config/terraform-mssql.tfvars \
-a /opt/automation/automation-mssql-linux/config/settings-mssql.yml \
-v
popd > /dev/null