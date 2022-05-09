from pyVmomi import vim
from typing import List

from .vsphere_base import VSphereBase
from .vsphere_datastore import VSphereDatastore
from .vsphere_host import VSphereHost
from .vsphere_network import VSphereNetwork
from .vsphere_resource_pool import VSphereResourcePool


class VSphereCluster(VSphereBase):
    def __init__(self, cluster: vim.ClusterComputeResource, **kwargs):
        if not isinstance(cluster, vim.ClusterComputeResource):
            raise ValueError(
                f"Parameter 'cluster' is not of type 'vim.ClusterComputeResource'"
            )
        super().__init__(name=cluster.name, **kwargs)

        # Internal variables
        self.__vim_cluster = cluster
        self.__hosts = None
        self.__datastores = None
        self.__networks = None
        self.__resource_pools = None

    @property
    def hosts(self) -> List[VSphereHost]:
        if not self.__hosts:
            self.__hosts = sorted(
                [VSphereHost(host=entity) for entity in self.__vim_cluster.host],
                key=lambda x: x.name,
            )
        return self.__hosts

    def find_host(self, name: str) -> VSphereHost:
        return next((x for x in self.hosts if x.name == name), None)

    @property
    def datastores(self) -> List[VSphereDatastore]:
        if not self.__datastores:
            self.__datastores = sorted(
                [
                    VSphereDatastore(datastore=entity)
                    for entity in self.__vim_cluster.datastore
                ],
                key=lambda x: x.name,
            )
        return self.__datastores

    def find_datastore(self, name: str) -> VSphereDatastore:
        return next((x for x in self.datastores if x.name == name), None)

    @property
    def networks(self) -> List[VSphereNetwork]:
        if not self.__networks:
            self.__networks = sorted(
                [
                    VSphereNetwork(network=entity)
                    for entity in self.__vim_cluster.network
                ],
                key=lambda x: x.name,
            )
        return self.__networks

    def find_network(self, name: str) -> VSphereNetwork:
        return next((x for x in self.networks if x.name == name), None)

    @property
    def resource_pools(self) -> List[VSphereResourcePool]:
        if not self.__resource_pools:
            self.__resource_pools = sorted(
                [
                    VSphereResourcePool(resource_pool=entity)
                    for entity in self.__vim_cluster.resourcePool.resourcePool
                ],
                key=lambda x: x.name,
            )
        return self.__resource_pools

    def find_resource_pool(self, name: str) -> VSphereResourcePool:
        return next(
            (x for x in self.resource_pools if x.name == name),
            None,
        )
