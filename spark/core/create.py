import os
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader

from spark.core import SPARK_CONFIG_FILE, EXPLICIT_INCLUSION_RULES


@dataclass
class CreateCommand:
    template: str
    output: str
    context: dict


class CreateUseCase:
    def execute(self, command):
        self._create(
            self._abs_path(command.output),
            command.template,
            command.output,
            command.context,
        )

    def _create(self, base_output_path, template, output, context):
        for name in os.listdir(template):
            template_path = os.path.join(template, name)
            output_path = os.path.join(output, name)

            if os.path.isdir(template_path) and self._should_exist(
                base_output_path, context, output_path
            ):
                os.makedirs(output_path)
                self._create(base_output_path, template_path, output_path, context)
            elif (
                os.path.isfile(template_path)
                and name != SPARK_CONFIG_FILE
                and self._should_exist(base_output_path, context, output_path)
            ):
                self._render_template(template_path, output_path, context)

    def _render_template(self, template_path, output_path, context):
        parent_folder = self._abs_path(os.path.join(template_path, ".."))
        jinja_env = Environment(
            loader=FileSystemLoader(parent_folder),
            trim_blocks=True,
            keep_trailing_newline=True,
        )
        name = os.path.basename(template_path)
        template = jinja_env.get_template(name)
        with open(output_path, "w") as fh:
            fh.write(template.render(**context))

    def _should_exist(self, base_output_path, context, output_path):
        relative_output_path = self._abs_path(output_path).replace(
            os.path.join(base_output_path, ""), ""
        )
        return context.get(EXPLICIT_INCLUSION_RULES, {}).get(relative_output_path, True)

    def _abs_path(self, path):
        return os.path.abspath(path)
