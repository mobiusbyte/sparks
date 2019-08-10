class ContextUserInterface:
    def __init__(self, prompter, default_config, skip_prompt):
        self._prompter = prompter
        self._skip_prompt = skip_prompt
        self._default_config = default_config

    def resolve_spark_config(self):
        if self._skip_prompt:
            return self._default_config
        else:
            spark_config = {}
            for key, default_value in self._default_config.items():
                spark_config[key] = self._prompter.prompt(
                    key, default_value=default_value
                )
            return spark_config
