import os
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader


@dataclass
class CreateCommand:
    template: str
    output: str
    context: dict


class CreateUseCase:
    def execute(self, command):
        self._create(command.template, command.output, command.context)

    def _create(self, template, output, context):
        for name in os.listdir(template):
            template_path = os.path.join(template, name)
            output_path = os.path.join(output, name)

            if os.path.isdir(template_path):
                os.makedirs(output_path)
                self._create(template_path, output_path, context)
            elif os.path.isfile(template_path):
                self._render_template(template_path, output_path, context)

    def _render_template(self, template_path, output_path, context):
        parent_folder = os.path.abspath(os.path.join(template_path, ".."))
        jinja_env = Environment(
            loader=FileSystemLoader(parent_folder),
            trim_blocks=True,
            keep_trailing_newline=True,
        )
        name = os.path.basename(template_path)
        template = jinja_env.get_template(name)
        with open(output_path, "w") as fh:
            fh.write(template.render(**context))
