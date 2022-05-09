from pyVmomi import vim

from .vsphere_base import VSphereBase


class VSphereDatastore(VSphereBase):
    def __init__(self, datastore: vim.Datastore, **kwargs):
        if not isinstance(datastore, vim.Datastore):
            raise ValueError(f"Parameter 'datastore' is not of type 'vim.Datastore'")
        super().__init__(name=datastore.name, **kwargs)

        # Internal variables
        self.__vim_datastore = datastore
