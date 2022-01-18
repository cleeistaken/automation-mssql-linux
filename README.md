# Microsoft SQL Server AG with Pacemaker

This project deploys and configures a Microsoft SQL Server AG cluster. 

## Requirements
The code was tested using the following versions.
* Python 3.6.8
* Ansible 2.11.7
* Terraform v1.1.3
* CentOS 8.5

## Known Issues
* Terraform may encounter an error while trying to customize Ubuntu VM running in vCenter 6.7. The solution is to upgrade to a newer version of vCenter. We have confirmed this issue occurs with vCenter 6.7.0.20000 (build 10244857). We have confirmed the customization works correctly with vCenter 6.7.0.47000 (build 17712750 ). 
https://github.com/hashicorp/terraform-provider-vsphere/issues/388