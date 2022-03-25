from pyVmomi import vim
from typing import List

from .vsphere_base import VSphereBase
from .vsphere_cluster import VSphereCluster


class VSphereDatacenter(VSphereBase):
    def __init__(self, datacenter: vim.Datacenter, **kwargs):
        if not isinstance(datacenter, vim.Datacenter):
            raise ValueError(f"Parameter 'datacenter' is not of type 'vim.Datacenter'")
        super().__init__(name=datacenter.name, **kwargs)

        # Internal variables
        self.__vim_datacenter = datacenter
        self.__clusters = None
        self.__folders = None

    @property
    def clusters(self) -> List[VSphereCluster]:
        if not self.__clusters:
            self.__clusters = sorted(
                [
                    VSphereCluster(cluster=entity)
                    for entity in self.__vim_datacenter.hostFolder.childEntity
                ],
                key=lambda x: x.name,
            )
        return self.__clusters

    def find_cluster(self, name: str) -> VSphereCluster:
        return next((x for x in self.clusters if x.name == name), None)

    @property
    def folders(self) -> List[VSphereCluster]:
        if not self.__folders:
            self.__folders = sorted(
                [
                    VSphereCluster(cluster=entity)
                    for entity in self.__vim_datacenter.hostFolder.childEntity
                ],
                key=lambda x: x.name,
            )
        return self.__clusters

    def find_folders(self, name: str) -> VSphereCluster:
        return next((x for x in self.clusters if x.name == name), None)
