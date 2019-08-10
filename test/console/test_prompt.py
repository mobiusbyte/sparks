from spark.console.prompt import ContextUserInterface
from test import fixture_path


class PrompterDouble:
    def __init__(self):
        self.answers = {"roses": "dark red", "violets": "blue-ish"}

        self.total_calls = 0

    def prompt(self, question, default, type):
        self.total_calls += 1
        return self.answers.get(question)


class TestContextUserInterface:
    def setup(self):
        self._default_config = fixture_path("sample_spark_config.yaml")

    def test_resolve_spark_config(self):
        prompter = PrompterDouble()

        ui = ContextUserInterface(prompter, self._default_config, skip_prompt=False)
        spark_config = ui.resolve_spark_config()

        assert prompter.total_calls == 2
        assert spark_config == prompter.answers

    def test_resolve_spark_config_skip(self):
        ui = ContextUserInterface(
            PrompterDouble(), self._default_config, skip_prompt=True
        )

        assert ui.resolve_spark_config() == {"roses": "red", "violets": "blue"}
