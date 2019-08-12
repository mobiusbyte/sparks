import os

import click

from sparks.console.commands import command_name
from sparks.console.prompt import ContextUserInterface
from sparks.core.create import CreateCommand, CreateUseCase, SPARK_CONFIG_FILE


@click.command(name=command_name(__name__))
@click.option(
    "--template",
    "-t",
    prompt="Template folder",
    help="Template folder to generate from",
)
@click.option(
    "--output",
    "-o",
    prompt="Output folder",
    help="Output folder to create files in. The folder will be created "
    "if it does not already exist.",
)
@click.option(
    "--skip-prompt",
    is_flag=True,
    help="Skip the prompt and use the default settings as specified "
    "in the `spark_config.yaml`.",
)
def command(template, output, skip_prompt):
    spark_config_file = os.path.expanduser(os.path.join(template, SPARK_CONFIG_FILE))
    ui = ContextUserInterface(click, spark_config_file, skip_prompt)
    context = ui.resolve_spark_config()

    if not os.path.isdir(output):
        os.makedirs(output)

    CreateUseCase().execute(
        command=CreateCommand(template=template, output=output, context=context)
    )
