import os

import pytest

from spark.console.prompt import ContextUserInterface
from test import fixture_path, assert_dicts


class PrompterDouble:
    def __init__(self, answers):
        self._answers = answers
        self.total_calls = 0

    def prompt(self, question, default, type):
        self.total_calls += 1
        return self._answers.get(question)


class TestContextUserInterface:
    def test_resolve_spark_config(self):
        prompter = PrompterDouble({"roses": "dark red", "violets": "blue-ish"})

        ui = ContextUserInterface(
            prompter, config_path("simple.yaml"), skip_prompt=False
        )
        spark_config = ui.resolve_spark_config()

        assert prompter.total_calls == 2
        assert_dicts(
            spark_config,
            {
                "roses": "dark red",
                "violets": "blue-ish",
                "explicit_inclusion_rules": {},
            },
        )

    def test_resolve_spark_config_skip(self):
        prompter = PrompterDouble({"roses": "dark red", "violets": "blue-ish"})
        ui = ContextUserInterface(
            prompter, config_path("simple.yaml"), skip_prompt=True
        )

        assert_dicts(
            ui.resolve_spark_config(),
            {"roses": "red", "violets": "blue", "explicit_inclusion_rules": {}},
        )

    @pytest.mark.parametrize(
        "answers, expected_config",
        [
            pytest.param(
                {"include_optional_files": True, "include_optional_folder": True},
                {
                    "include_optional_files": True,
                    "include_optional_folder": True,
                    "explicit_inclusion_rules": {
                        "first/optional_folder": True,
                        "first/optional_folder/another_optional_file": True,
                        "second/optional_file.txt": True,
                    },
                },
            ),
            pytest.param(
                {"include_optional_files": False, "include_optional_folder": True},
                {
                    "include_optional_files": False,
                    "include_optional_folder": True,
                    "explicit_inclusion_rules": {
                        "first/optional_folder": True,
                        "first/optional_folder/another_optional_file": False,
                        "second/optional_file.txt": False,
                    },
                },
            ),
            pytest.param(
                {"include_optional_files": True, "include_optional_folder": False},
                {
                    "include_optional_files": True,
                    "include_optional_folder": False,
                    "explicit_inclusion_rules": {
                        "first/optional_folder": False,
                        "first/optional_folder/another_optional_file": True,
                        "second/optional_file.txt": True,
                    },
                },
            ),
            pytest.param(
                {"include_optional_files": False, "include_optional_folder": False},
                {
                    "include_optional_files": False,
                    "include_optional_folder": False,
                    "explicit_inclusion_rules": {
                        "first/optional_folder": False,
                        "first/optional_folder/another_optional_file": False,
                        "second/optional_file.txt": False,
                    },
                },
            ),
        ],
    )
    def test_resolve_spark_config_with_rules(self, answers, expected_config):
        prompter = PrompterDouble(answers)

        ui = ContextUserInterface(
            prompter, config_path("with_rules.yaml"), skip_prompt=False
        )

        assert_dicts(ui.resolve_spark_config(), expected_config)


def config_path(name):
    return os.path.join(fixture_path("spark_configs"), name)
