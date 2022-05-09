from pyVmomi import vim

from .vsphere_base import VSphereBase


class VSphereResourcePool(VSphereBase):
    def __init__(self, resource_pool: vim.ResourcePool, **kwargs):
        if not isinstance(resource_pool, vim.ResourcePool):
            raise ValueError(
                f"Parameter 'resource_pool' is not of type 'vim.ResourcePool'"
            )
        super().__init__(name=resource_pool.name, **kwargs)

        # Internal variables
        self.__vim_resource_pool = resource_pool
