from pyVmomi import vim

from vsphere_base import VSphereBase


class VSphereVm(VSphereBase):
    def __init__(self, vm: vim.VirtualMachine, **kwargs):
        if not isinstance(vm, vim.VirtualMachine):
            raise ValueError(f"Parameter 'vm' is not of type 'vim.VirtualMachine'")
        super().__init__(name=vm.name, **kwargs)

        # Internal variables
        self.__vim_vm = vm
