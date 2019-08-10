import click

from spark.console.commands import command_name
from spark.core.create import CreateCommand, CreateUseCase


@click.command(name=command_name(__name__))
@click.option(
    "--template", prompt="Template folder", help="Template folder to generate from"
)
@click.option(
    "--output", prompt="Output folder", help="Output folder to create files in"
)
def command(template, output):
    CreateUseCase().execute(command=CreateCommand(template=template, output=output))
