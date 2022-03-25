from pyVmomi import vim
from typing import List

from .vsphere_base import VSphereBase
from .vsphere_datastore import VSphereDatastore
from .vsphere_network import VSphereNetwork


class VSphereHost(VSphereBase):
    def __init__(self, host: vim.HostSystem, **kwargs):
        if not isinstance(host, vim.HostSystem):
            raise ValueError(f"Parameter 'host' is not of type 'vim.HostSystem'")
        super().__init__(name=host.name, **kwargs)

        # Internal variables
        self.__vim_host = host
        self.__datastores = None
        self.__networks = None

    @property
    def datastores(self) -> List[VSphereDatastore]:
        if not self.__datastores:
            self.__datastores = sorted(
                [
                    VSphereDatastore(datastore=entity)
                    for entity in self.__vim_host.datastore
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
                [VSphereNetwork(network=entity) for entity in self.__vim_host.network],
                key=lambda x: x.name,
            )
        return self.__networks

    def find_network(self, name: str) -> VSphereNetwork:
        return next(
            (x for x in self.networks if x.name == name),
            None,
        )
