import os
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader, Template

from sparks.core import SPARK_CONFIG_FILE, CREATION_RULES


PATH_FOLDER = "folder"
PATH_FILE = "file"


@dataclass
class CreateCommand:
    template: str
    output: str
    context: dict


class CreateResolver:
    def __init__(self, base_template_folder, context):
        self._context = context
        self._base_template_folder = base_template_folder
        self._handlers = {
            PATH_FILE: self._handle_file,
            PATH_FOLDER: self._handle_folder,
        }

    def create(self, template, base_output_folder):
        for path_type, template_path in self._list_dir(template):
            if self._should_create(template_path):
                output_path = os.path.join(
                    base_output_folder,
                    self._rendered_name(template_path, self._context),
                )
                self._handlers[path_type](template_path, output_path)

    @staticmethod
    def _list_dir(template):
        for name in os.listdir(template):
            template_path = os.path.join(template, name)

            if os.path.isdir(template_path):
                yield PATH_FOLDER, template_path
            elif os.path.isfile(template_path) and name != SPARK_CONFIG_FILE:
                yield PATH_FILE, template_path

    def _should_create(self, template_path):
        relative_template_path = self._abs_path(template_path).replace(
            os.path.join(self._base_template_folder, ""), ""
        )

        return self._context.get(CREATION_RULES, {}).get(relative_template_path, True)

    def _rendered_name(self, template_path, context):
        name = os.path.basename(template_path)
        return Template(name).render(**context)

    def _handle_folder(self, template_path, output_path):
        os.makedirs(output_path)
        self.create(template_path, output_path)

    def _handle_file(self, template_path, output_path):
        jinja_env = self._jinja_env(template_path)
        name = os.path.basename(template_path)

        template = jinja_env.get_template(name)
        with open(output_path, "w") as fh:
            fh.write(template.render(**self._context))

    def _jinja_env(self, template_path):
        parent_folder = self._abs_path(os.path.join(template_path, ".."))

        return Environment(
            loader=FileSystemLoader(parent_folder),
            trim_blocks=True,
            keep_trailing_newline=True,
        )

    def _abs_path(self, path):
        return os.path.abspath(path)


class CreateUseCase:
    def execute(self, command):
        resolver = CreateResolver(os.path.abspath(command.template), command.context)
        resolver.create(command.template, command.output)
