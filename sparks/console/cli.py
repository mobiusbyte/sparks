import click
from importlib import import_module


command_registry = ["create"]


@click.group("sparks")
def cli():
    pass


for entry in command_registry:
    command_module = f"sparks.console.commands.{entry}"
    module = import_module(command_module)
    cli.add_command(getattr(module, "command"))


def main():
    cli()
