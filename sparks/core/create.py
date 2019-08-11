import os
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader, Template

from sparks.core import SPARK_CONFIG_FILE, CREATION_RULES


@dataclass
class CreateCommand:
    template: str
    output: str
    context: dict


class CreateUseCase:
    def execute(self, command):
        self._create(
            self._abs_path(command.template),
            command.template,
            command.output,
            command.context,
        )

    def _create(self, base_template_path, template, output, context):
        for name in os.listdir(template):
            template_path = os.path.join(template, name)
            output_path = os.path.join(output, self._rendered_name(name, context))

            if os.path.isdir(template_path) and self._should_create(
                base_template_path, context, template_path
            ):
                os.makedirs(output_path)
                self._create(base_template_path, template_path, output_path, context)
            elif (
                os.path.isfile(template_path)
                and name != SPARK_CONFIG_FILE
                and self._should_create(base_template_path, context, template_path)
            ):
                self._render_template(template_path, output_path, context)

    def _abs_path(self, path):
        return os.path.abspath(path)

    def _rendered_name(self, name, context):
        return Template(name).render(**context)

    def _should_create(self, base_template_path, context, template_path):
        relative_template_path = self._abs_path(template_path).replace(
            os.path.join(base_template_path, ""), ""
        )

        return context.get(CREATION_RULES, {}).get(relative_template_path, True)

    def _render_template(self, template_path, output_path, context):
        jinja_env = self._jinja_env(template_path)
        name = os.path.basename(template_path)

        template = jinja_env.get_template(name)
        with open(output_path, "w") as fh:
            fh.write(template.render(**context))

    def _jinja_env(self, template_path):
        parent_folder = self._abs_path(os.path.join(template_path, ".."))

        return Environment(
            loader=FileSystemLoader(parent_folder),
            trim_blocks=True,
            keep_trailing_newline=True,
        )
