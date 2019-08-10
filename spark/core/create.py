import os
from dataclasses import dataclass
from shutil import copyfile


@dataclass
class CreateCommand:
    template: str
    output: str


class CreateUseCase:
    def execute(self, command):
        self._create(command.template, command.output)

    def _create(self, template, output):
        for name in os.listdir(template):
            template_path = os.path.join(template, name)
            output_path = os.path.join(output, name)

            if os.path.isdir(template_path):
                os.makedirs(output_path)
                self._create(template_path, output_path)
            elif os.path.isfile(template_path):
                copyfile(template_path, output_path)
