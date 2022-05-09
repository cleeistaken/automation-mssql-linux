from pyVmomi import vim

from .vsphere_base import VSphereBase


class VSphereNetwork(VSphereBase):
    def __init__(self, network: vim.Network, **kwargs):
        if not isinstance(network, vim.Network):
            raise ValueError(f"Parameter 'network' is not of type 'vim.Network'")
        super().__init__(name=network.name, **kwargs)

        # Internal variables
        self.__vim_network = network
