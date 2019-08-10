import yaml


class ContextUserInterface:
    def __init__(self, prompter, config_file, skip_prompt):
        self._prompter = prompter
        self._default_config = self._default_config(config_file)
        self._skip_prompt = skip_prompt

    def resolve_spark_config(self):
        if self._skip_prompt:
            return self._default_config
        else:
            spark_config = {}
            for key, default_value in self._default_config.items():
                spark_config[key] = self._prompter.prompt(
                    key, default=default_value, type=type(default_value)
                )
            return spark_config

    def _default_config(self, config_file):
        with open(config_file, "rb") as fh:
            return yaml.safe_load(fh)
