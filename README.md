# Microsoft SQL Server AG with Pacemaker

This project deploys a Microsoft SQL Server on Linux cluster, using Always On Availability Group, with Pacemaker, Corosync and the STONITH fencing component (vmw_fence_rest).

## Use Case
Microsoft SQL Server on Linux is a version of the well-known enterprise-grade RDBM from Microsoft. Unlike the traditional Microsoft SQL Server, this version runs entirely on the Linux Operating System platforms.

Like most enterprise-level applications, Microsoft SQL Server requires a certain level of assurance of availability, resilience and recoverability in the event of a component failure or a disaster event. The Always On clustering option is Microsoft’s solution for this requirement in the Microsoft SQL Server space.

Microsoft SQL Server on Linux uses several third-party Tools and Solutions to achieve High Availability for its instances. These include Pacemaker, Corosync, STONITH, etc. 

As Microsoft SQL Server on Linux continues to gain traction and become well-accepted in the enterprise, many Microsoft SQL Server and VMware Infrastructure Administrators have directly and indirectly requested for guidance on how to successfully configure and run clustered instances of Microsoft SQL Server on Linux and the required external components on the vSphere platforms.

The Solution presented in this Package includes all the necessary configuration tasks, steps and processes required to automate the deployment of a single prototype, non-Production cluster of up to nine (9) fully-installed, up-to-date Microsoft SQL Server Nodes, running on Ubuntu Linux and configured in a single Availability Group configuration – with just a few configuration parameters supplied by the Administrator.

This Package is released without any guarantee of fit or official support. It is not intended to replace any corporate administrative practices, nor are the deployed VMs expected to be used for Production workloads without undergoing additional rigorous auditing and configurations deemed necessary by the end-user.

We hope this Package will serve as a useful starting point and building block for all Microsoft SQL Server Administrators who may have been struggling with getting similar Solutions successfully deployed or have been wondering if it’s “doable on vSphere”.


## Requirements
The code was tested using the following Tools, OSes, and Application versions. Although not extensively tested, these scripts may work with other versions.

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
The recommended method of running this code is using our preconfigured ova template. The template is built on a minimal Centos Stream 9 Linux distribution and contains all the required packages, including the Ubuntu 20.04.03 template used to create the MSSQL VMs.

### Appliance
1. Download the .OVA template.

   https://storage.googleapis.com/workload-automation/templates/testbench-1.2.1.ova
   https://storage.googleapis.com/workload-automation/templates/testbench-1.3.0rc1.ova


2. Deploy the template. During the deployment configure the following:
   * root password
   * DHCP or Static network configuration
   * IPv4 parameters (if Static network configuration)

### Configure
1. Login as ***root***

2. Edit the **terraform-mssql.tfvars** file. This file contains information about the vSphere environment. This is the primary files used by Terraform.
    ```console
    cd /opt/automation/automation-mssql-linux/config/
    vi terraform-mssql.tfvars
    ```   

3. Edit the **settings-mssql.yml** file. This file contains information about the MSSQL cluster to be created. This is the primary file used by Ansible. 
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

#### Deploy
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

#### Destroy
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
* After a failed deployment, trying to deploy again may generate the following error. If this happens, it is necessary to destroy, revalidate, and try the deployment again.
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


* An issue with **vmw_fence_rest** STONITH configuration parameters. We observed that, on some vSphere Versions (e.g. 6.7.0 - Build 18010599), the value supplied for “vcenter_server” must be the IP address of the vCenter Server. Specifying the FQDN of the vCenter Server results in failed STONITH configuration.

## Authors

* Deji Akomolafe is a VMware Staff Solutions Architect that specializes in the virtualization of Microsoft Business Critical Applications on VMware's vSphere.

* Mark Xu is a VMware Solutions Architect that specializes in Business Critical Applications Solutions on VMware's vSphere.

* Charles Lee is a VMware Senior Solutions Architect that specializes in Business Critical Application and Automation on VMware's vSphere.


# Changelog
### 1.0 
* Initial release.

### 1.1
* Improve the ovf configuration script
* Improve the template preparation script

### 1.2
* Add anti-affinity rule for MSSQL VM
* Add second disk to the MSSQL VM and use it as the log disk
* Fixed ansible apt update statement failing because of an upstream repository change

### 1.2.1
* Add parameters to the AG creation
  * DTC_SUPPORT = NONE
  * AUTOMATED_BACKUP_PREFERENCE = SECONDARY_ONLY
  * REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT = 1
  * BACKUP_PRIORITY = 50
  * SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY)

### 1.3.0RC1
* Improved the validation script
* Added an HTTP GUI
