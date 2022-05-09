from abc import ABC, abstractmethod
from typing import List, Callable


class ConfigBase(ABC):
    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", False)
        self.verbose = kwargs.get("verbose", False)

    def _is_set(self, x: str) -> bool:
        return hasattr(self, x) and self.__getattribute__(x) is not None

    def _check_is_set(self, x: str) -> bool:
        if self.verbose:
            print(f"Checking variable '{x}' set... ", end="")
        if self._is_set(x):
            if self.verbose:
                print("OK")
            return True
        else:
            if self.verbose:
                print("ERROR")
            return False

    def _check_type(self, x: str, f: Callable) -> bool:
        if self._is_set(x):
            y = self.__getattribute__(x)
            if self.verbose:
                print(f"Checking variable '{x}' type... ", end="")
            if f(y):
                if self.verbose:
                    print("OK")
                return True
            else:
                if self.verbose:
                    print("ERROR")
                return False

    def _check_value(self, x: str, f: Callable) -> bool:
        if self._is_set(x) and f:
            y = self.__getattribute__(x)
            if self.verbose:
                print(f"Checking variable '{x}' value... ", end="")
            if f(y):
                if self.verbose:
                    print("OK")
                return True
            else:
                if self.verbose:
                    print("ERROR")
                return False

    def _check_validation_data(self, items: List[dict]) -> List[str]:
        errors = []
        for item in items:
            var = item.get("variable")
            var_d = item.get("variable_description")
            type_f = item.get("type")
            type_d = item.get("type_name")
            value_f = item.get("value")
            value_d = item.get("value_description")

            if not self._check_is_set(var):
                errors.append(f"{var_d} ({var}) is not set.")
            else:
                if not self._check_type(var, type_f):
                    errors.append(f"{var_d} ({var}) is not of type '{type_d}'")
                if value_f:
                    if not self._check_value(var, value_f):
                        errors.append(f"{var_d} ({var}) value is not {value_d}")
        return errors

    @abstractmethod
    def open(self, **kwargs):
        pass

    @abstractmethod
    def write(self, **kwargs):
        pass

    @abstractmethod
    def validate(self) -> List[str]:
        pass

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f"Parameter is not of type 'bool'")
        self.__verbose = value

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f"Parameter is not of type 'bool'")
        self.__debug = value
