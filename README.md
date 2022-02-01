# Microsoft SQL Server AG with Pacemaker

This project deploys a Microsoft SQL Server AG cluster with Pacemaker and stonith fence.

## Use Case
Microsoft SQL Server on Linux is a version of the well-known enterprise-grade RDBM from Microsoft. Unlike the traditional Microsoft SQL Server, this version runs entirely on the Linux Operating System platforms.

Like most enterprise-level applications, Microsoft SQL Server requires a certain level of assurance of availability, resilience and recoverability in the event of a component failure or a disaster event. The Always On clustering option is Microsoft’s solution for this requirement in the Microsoft SQL Server space.

Microsoft SQL Server on Linux uses several third-party Tools and Solutions to achieve High Availability for its instances. These include Pacemaker, Corosync, STONITH, etc. 

As Microsoft SQL Server on Linux continues to gain traction and become well-accepted in the enterprise, many Microsoft SQL Server and VMware Infrastructure Administrators have directly and indirectly requested for guidance on how to successfully configure and run clustered instances of Microsoft SQL Server on Linux and the required external components on the vSphere platforms.

The Solution presented in this Package includes all the necessary configuration tasks, steps and processes required to automate the deployment of a single prototype, non-Production cluster of up to nine (9) fully-installed, up-to-date Microsoft SQL Server Nodes, running on Ubuntu Linux and configured in a single Availability Group configuration – with just a few configuration parameters supplied by the Administrator.

This Package is released without any guarantee of fit or official support. It is not intended to replace any corporate administrative practices, nor are the deployed VMs expected to be used for Production workloads without undergoing additional rigorous auditing and configurations deemed necessary by the end-user.

Our hope is that the Package will serve as a useful starting point and building block for all Microsoft SQL Server Administrators who may have been struggling with getting similar Solutions successfully deployed or have been wondering if it’s “doable on vSphere”.


## Requirements
The code was tested using the following Tools, OSes, and Application versions. Although not extensively tested these scripts may work with other versions.

### vSphere Environment
* vSphere 6.7U3 (6.7.0.47000)
* vSphere 7.0

### Automation System
* Python 3.9.9
* Terraform 1.1.4
* CentOS Stream 9

### Python 3 packages
* ansible 5.2.0
* ansible-core 2.12.2 

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
* Terraform resource pool creation will fail if VMware Distributed Resource Scheduler DRS is not enabled on the cluster. 

  https://www.vmware.com/products/vsphere/drs-dpm.html


* Terraform may encounter an error while trying to customize Ubuntu VM running in vCenter 6.7. This is a known issue with earlier release of vSphere 6.7. The solution is an upgrade to a newer version of vCenter. 
  * We have confirmed this issue occurs with vCenter 6.7.0.20000 (build 10244857). 
  * We have confirmed the customization works correctly with vCenter 6.7.0.47000 (build 17712750 ).

  https://github.com/hashicorp/terraform-provider-vsphere/issues/388


* Deployments to an NFS datastore may fail at various stages. This issue is under investigation. For the time being it is recommended to deploy to a vSAN, FC, or iSCSI datastore. 

## Troubleshooting
* After a failed deployment trying to deploy again may generate the following error. If this happens it is necessary to destroy, revalidate, and try the deployment again.
    ```
    Applying Terraform using tfplan
    ╷
    │ Error: Saved plan is stale
    │
    │ The given plan file can no longer be applied because the state was changed by another operation after the plan was
    │ created.
    ```

* A failed deployment may leave incompletely created resources in vCenter. If this happens both deployment and destruction may fail. If this happens it is necessary to manually delete the following resources in vCenter:
  * Content library (default: **Content Library MSSQL**)
  * Virtual machine folder (default: **mssql**)
  * Virtual machines (default: **mssql-linux-xx**)
  * Resource pool (default: **mssql**)