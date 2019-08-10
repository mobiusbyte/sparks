import click
from importlib import import_module


command_registry = ["create"]


@click.group("spark")
def cli():
    pass


for entry in command_registry:
    command_module = f"spark.console.commands.{entry}"
    module = import_module(command_module)
    cli.add_command(getattr(module, "command"))


def main():
    cli()
