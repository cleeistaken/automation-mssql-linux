import click
from jinja2 import TemplateNotFound
from lark.exceptions import UnexpectedToken
from yaml.parser import ParserError

from src.mssql_linux import MssqlLinux

VERSION = "0.0.1"


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass


@cli.command("prompt")
@click.option("-a", "--ansible", type=click.Path(exists=False), required=True)
@click.option("-t", "--terraform", type=click.Path(exists=False), required=True)
@click.option("-v", "--verbose", is_flag=True)
def mssql_prompt(ansible: str, terraform: str, verbose: bool):
    try:
        tc = MssqlLinux(verbose=verbose)
        tc.prompt()

        print("Validating the configuration parameters.")
        errors = tc.validate()
        if not errors:
            print("Configuration is valid.")
        else:
            print("\nWarning! The following issues were found:")
            for error in errors:
                print(f"- {error}")

        print("Saving configuration files.")
        tc.write(terraform_file=terraform, ansible_file=ansible)

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    except TemplateNotFound as e:
        print(f"Error: Could not find template file '{e}'")
        exit(1)


@cli.command("validate")
@click.option("-a", "--ansible", type=click.Path(exists=True), required=True)
@click.option("-t", "--terraform", type=click.Path(exists=True), required=True)
@click.option("-v", "--verbose", is_flag=True)
def mssql_validate(ansible: str, terraform: str, verbose: bool):
    try:
        tc = MssqlLinux(verbose=verbose)
        tc.open(terraform_file=terraform, ansible_file=ansible)

        print("Validating the configuration parameters.")
        errors = tc.validate()
        if not errors:
            print("Configurations are valid.")
        else:
            print("\nWarning! The following issues were found:")
            for error in errors:
                print(f"- {error}")
            exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except UnexpectedToken:
        print(
            f"Error: Unable to parse terraform file. Is it a valid terraform hcl2 file?"
        )
        exit(1)
    except ParserError:
        print(f"Error: Unable to parse ansible file. Is it a valid ansible yaml file?")
        exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
