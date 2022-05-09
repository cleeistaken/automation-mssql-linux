# https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi
import re
from ipaddress import IPv4Address
from typing import List

import inquirer
import inquirer.errors


def find_obj_name(object_list: list, name: str):
    return next((x for x in object_list if x.name == name), None)


# noinspection PyUnusedLocal
def validation_ipv4_cidr(answers, current):
    pattern = (
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        r"(\/([0-9]|[1-2][0-9]|3[0-2]))?$"
    )
    if not re.match(pattern, current):
        raise inquirer.errors.ValidationError(
            "", reason="Not a valid IPv4 CIDR notation."
        )
    return True


# noinspection PyUnusedLocal
def validation_ipv4_address(answers, current):
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if not re.match(pattern, current):
        raise inquirer.errors.ValidationError("", reason="Not a valid IPv4 address.")
    return True


# noinspection PyUnusedLocal
def validation_ipv4_address_list(answers, current):
    pattern = (
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)?"
        r"(,\s*(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)?)*$"
    )
    if not re.match(pattern, current):
        raise inquirer.errors.ValidationError(
            "", reason="Not a valid IPv4 address list."
        )
    return True


# https://validators.readthedocs.io/en/latest/_modules/validators/domain.html#domain
# noinspection PyUnusedLocal
def validation_domain(answers, current):
    pattern = (
        r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\."
        r"([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$"
    )
    if not re.match(pattern, current):
        raise inquirer.errors.ValidationError("", reason="Not a valid domain.")
    return True


# noinspection PyUnusedLocal
def validation_domain_list(answers, current):
    pattern = (
        r"^((([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\."
        r"([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3}))"
        r"(,\s*((([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\."
        r"([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3}))+)*$"
    )
    if not re.match(pattern, current):
        raise inquirer.errors.ValidationError("", reason="Not a valid domain list.")
    return True


# noinspection PyUnusedLocal
def validation_vcpu(answers, current):
    if int(current) < 1 or int(current) > 128:
        raise inquirer.errors.ValidationError("", reason="Not a valid vCPU count.")
    return True


# noinspection PyUnusedLocal
def validation_memory(answers, current):
    if int(current) < 4 or int(current) > 1024:
        raise inquirer.errors.ValidationError("", reason="Not a valid memory size.")
    return True


# noinspection PyUnusedLocal
def validation_disk(answers, current):
    if int(current) < 40:
        raise inquirer.errors.ValidationError("", reason="Not a valid disk size.")
    return True


def str_to_list_ipaddress(string: str) -> List[IPv4Address]:
    return [IPv4Address(x.strip()) for x in string.split(",")]


# https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
def find_duplicates(data: List) -> List:
    seen = set()
    dupes = set()
    for x in data:
        if x in seen:
            dupes.add(x)
        else:
            seen.add(x)
    return list(dupes)
