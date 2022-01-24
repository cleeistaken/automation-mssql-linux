# Microsoft SQL Server AG with Pacemaker

This project deploys a Microsoft SQL Server AG cluster with Pacemaker and stonith fence.

## Requirements
The code was tested using the following versions.

### vSphere Environment
* vSphere 6.7U3 (6.7.0.47000)
* vSphere 7.0

### Automation System
* Python 3.6.8
* Terraform v1.1.3
* CentOS 8.5

### Python 3 packages
* ansible 4.10.0
* ansible-core 2.11.7 

### MSSQL VM Template
* Ubuntu 20.04.03 

## Procedure

### Configure
1. Login as ***root***

2. Edit the **terraform-mssql.tfvars** file. This file contains information about the vSphere environment. This is the primary files used by Terraform.
    ```console
    cd /opt/automation/automation-mssql-linux/config/
    vi terraform-mssql.tfvars
    ```   

3. Edit the **settings-mssql.yml** file. This file contains information about the MSSQL cluster to be created. The is the primary file used by Ansible. 
   * ***mssql_pid***
   * ***mssql_accept_eula*** 
   * ***mssql_pcs_cluster_vip_cidr***
    ```console
    cd /opt/automation/automation-mssql-linux/config/
    vi settings-mssql.yml
    ```

4. Validate the settings.
   ```console
   cd /opt/automation/automation-mssql-linux/
   ./validate.sh
   ```

### Deploy
1. Login as ***root***

2. Validate the settings.
   ```console
   cd /opt/automation/automation-mssql-linux/
   ./validate.sh
   ```

3. Deploy the environment.
   ```console
   cd /opt/automation/automation-mssql-linux/
   ./deploy.sh
   ```

### Destroy
1. Login as ***root*** 

2. Destroy the environment.
    ```console
    cd /opt/automation/automation-mssql-linux/
    ./destroy.sh
    ```   


## Known Issues / Limitations
* A failed deployment may leave incompletely created resources in vCenter. If this happens both deployment and destruction may fail. If this happens manually it is necessary to delete the following resources in vCenter:
  * Content library (default: **Content Library MSSQL**)
  * Virtual machines (default: **mssql-linux-xx**)
  * Resource pool (default: **mssql**)


* Terraform resource pool creation will fail if VMware Distributed Resource Scheduler DRS is not enabled on the cluster. 

  https://www.vmware.com/products/vsphere/drs-dpm.html


* Terraform may encounter an error while trying to customize Ubuntu VM running in vCenter 6.7. This is a known issue with earlier release of vSphere 6.7. The solution is an upgrade to a newer version of vCenter. 
  * We have confirmed this issue occurs with vCenter 6.7.0.20000 (build 10244857). 
  * We have confirmed the customization works correctly with vCenter 6.7.0.47000 (build 17712750 ).

  https://github.com/hashicorp/terraform-provider-vsphere/issues/388

