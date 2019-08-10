import yaml

from spark.core import EXPLICIT_INCLUSION_RULES


class ContextUserInterface:
    def __init__(self, prompter, config_file, skip_prompt):
        self._prompter = prompter
        self._default_config = self._default_config(config_file)
        self._skip_prompt = skip_prompt

    def resolve_spark_config(self):
        spark_config = {EXPLICIT_INCLUSION_RULES: {}}

        explicit_inclusion_rules = {}
        for key, default_value in self._default_config.items():
            if EXPLICIT_INCLUSION_RULES == key:
                explicit_inclusion_rules = default_value
            else:
                spark_config[key] = self._answer(key, default_value)

        for path, should_include in explicit_inclusion_rules.items():
            spark_config[EXPLICIT_INCLUSION_RULES][path] = spark_config.get(
                should_include
            )

        return spark_config

    def _default_config(self, config_file):
        with open(config_file, "rb") as fh:
            return yaml.safe_load(fh)

    def _answer(self, key, default_value):
        if self._skip_prompt:
            return default_value
        else:
            return self._prompter.prompt(
                key, default=default_value, type=type(default_value)
            )
