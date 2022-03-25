from pyVmomi import vim
from typing import List

from vsphere_base import VSphereBase
from vsphere_vm import VSphereVm


class VSphereFolder(VSphereBase):
    def __init__(self, folder: vim.Folder, **kwargs):
        if not isinstance(folder, vim.Folder):
            raise ValueError(f"Parameter 'folder' is not of type 'vim.Folder'")
        super().__init__(name=folder.name, **kwargs)

        # Internal variables
        self.__vim_folder = folder
        self.__folders = None
        self.__vms = None

    @property
    def folders(self) -> List["VSphereFolder"]:
        if not self.__folders:
            self.__folders = sorted(
                [
                    VSphereFolder(folder=entity)
                    for entity in self.__vim_folder.childEntity
                    if isinstance(entity, vim.Folder)
                ],
                key=lambda x: x.name,
            )
        return self.__folders

    def find_folders(self, name: str) -> "VSphereFolder":
        return next((x for x in self.folders if x.name == name), None)

    @property
    def vms(self) -> List[VSphereVm]:
        if not self.__vms:
            self.__vms = sorted(
                [
                    VSphereVm(vm=entity)
                    for entity in self.__vim_folder.childEntity
                    if isinstance(entity, vim.VirtualMachine)
                ],
                key=lambda x: x.name,
            )
        return self.__vms

    def find_vms(self, name: str) -> VSphereVm:
        return next((x for x in self.vms if x.name == name), None)
