from abc import ABC


class VSphereBase(ABC):
    def __init__(self, name: str, **kwargs):
        self.__debug = kwargs.get("debug", False)
        self.__verbose = kwargs.get("verbose", False)
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f"Name: {self.name}"

    def set_verbose(self, verbose: bool):
        if not isinstance(verbose, bool):
            raise ValueError(f"Parameter 'verbose' if not of type 'bool'")
        self.__verbose = verbose

    def set_debug(self, debug: bool):
        if not isinstance(debug, bool):
            raise ValueError(f"Parameter 'debug' if not of type 'bool'")
        self.__debug = debug

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"Parameter is not of type 'str'")
        self.__name = value
