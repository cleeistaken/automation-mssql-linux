import atexit
import socket
import ssl

from typing import List
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

from .vsphere_datacenter import VSphereDatacenter

VC_PORT_MIN = 1
VC_PORT_MAX = 65535


class VCenterServer:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        allow_insecure_ssl: bool = False,
        **kwargs,
    ):
        # Debug variables
        self.debug = kwargs.get("debug", False)
        self.verbose = kwargs.get("verbose", False)

        # vCenter variables
        self.host = host
        self.username = username
        self.password = password
        self.port = kwargs.get("port", 443)
        self.allow_insecure_ssl = allow_insecure_ssl

        # Internal variables
        self.__content = None
        self.__si = None
        self.__vim_uuid = None
        self.__version = None
        self.__build = None
        self.__datacenters = None

    def __repr__(self):
        return (
            f'server: "{self.host}" '
            f'username: "{self.username}" '
            f"port: {self.port} "
            f"verify_ssl: {self.allow_insecure_ssl}"
        )

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.disconnect()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.host == other.host
            and self.username == other.username
            and self.password == other.password
            and self.allow_insecure_ssl == other.allow_insecure_ssl
            and self.__content == other.__content
            and self.__si == other.__si
            and self.__vim_uuid == other.__vim_uuid
        )

    # noinspection PyProtectedMember
    def connect(self):
        if self.verbose:
            print(f"Connecting to '{self.host}' using '{self.username}'")

        # Create SSL context
        if self.allow_insecure_ssl and hasattr(ssl, "_create_unverified_context"):
            # noinspection PyProtectedMember
            context = ssl._create_unverified_context()
        else:
            context = None

        try:
            self.__si = SmartConnect(
                host=self.host,
                user=self.username,
                pwd=self.password,
                port=int(self.port),
                sslContext=context,
            )
        except socket.gaierror:
            raise ValueError(f"Unable to resolve vCenter server: '{self.host}'")
        except vim.fault.InvalidLogin:
            raise ValueError(f"Invalid credentials for vCenter server: '{self.host}'")

        # Make sure we are connected
        if not self.__si:
            raise RuntimeError(
                "Could not connect to the specified vCenter using specified username and password."
            )

        # Disconnect this thing on exit
        atexit.register(Disconnect, self.__si)

        # Retrieve the service content
        self.__content = self.__si.RetrieveContent()

        # Make sure wer retrieved the content
        if not self.__content:
            raise RuntimeError("Could not retrieve content from vCenter.")

        # Set vCenter parameters
        self.__vim_uuid = self.__content.about.instanceUuid
        self.__version = self.__content.about.version
        self.__build = self.__content.about.build

        if self.verbose:
            print(
                f"Connected to '{self.host}' with version: {self.__version} build: {self.__build}"
            )

    def disconnect(self):
        if self.__si:
            if self.verbose:
                print(f"Disconnecting from '{self.host}'")
            Disconnect(self.__si)
        self.__si = None
        self.__content = None
        self.__vim_uuid = None
        self.__version = None
        self.__build = None
        self.__datacenters = None

    @property
    def datacenters(self) -> List[VSphereDatacenter]:
        if not self.__datacenters:
            self.__datacenters = sorted(
                [
                    VSphereDatacenter(datacenter=entity)
                    for entity in self.__content.rootFolder.childEntity
                    if hasattr(entity, "vmFolder")
                ],
                key=lambda x: x.name,
            )
        return self.__datacenters

    def find_datacenter(self, name: str) -> VSphereDatacenter:
        return next((x for x in self.datacenters if x.name == name), None)

    def vim_uuid(self) -> str:
        return self.__vim_uuid

    def version(self) -> str:
        return self.__version

    def build(self) -> str:
        return self.__build

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
        if value < VC_PORT_MIN or value > VC_PORT_MAX:
            raise ValueError(
                f"Specified port is out of range [{VC_PORT_MIN}, {VC_PORT_MAX}]: {value}"
            )
        self._port = value

    @property
    def allow_insecure_ssl(self) -> bool:
        return self._allow_insecure_ssl

    @allow_insecure_ssl.setter
    def allow_insecure_ssl(self, value: bool):
        self._allow_insecure_ssl = value
