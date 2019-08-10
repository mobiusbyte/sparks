import os

import click

from spark.console.commands import command_name
from spark.console.prompt import ContextUserInterface
from spark.core.create import CreateCommand, CreateUseCase, SPARK_CONFIG_FILE


@click.command(name=command_name(__name__))
@click.option(
    "--template", prompt="Template folder", help="Template folder to generate from"
)
@click.option(
    "--output", prompt="Output folder", help="Output folder to create files in"
)
@click.option("--skip-prompt", is_flag=True)
def command(template, output, skip_prompt):
    spark_config_file = os.path.expanduser(os.path.join(template, SPARK_CONFIG_FILE))
    ui = ContextUserInterface(click, spark_config_file, skip_prompt)
    context = ui.resolve_spark_config()

    CreateUseCase().execute(
        command=CreateCommand(template=template, output=output, context=context)
    )
