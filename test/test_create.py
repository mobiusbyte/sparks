from shutil import rmtree

import pytest

from spark.core.create import CreateCommand, CreateUseCase
from test import expected_folder, assert_folder, template_folder, tmp_folder


class TestCreate:
    def setup(self):
        self._tmp_folder = tmp_folder()
        self._use_case = CreateUseCase()

    def teardown(self):
        rmtree(self._tmp_folder, ignore_errors=True)

    @pytest.mark.parametrize(
        "template, expected, context",
        [
            pytest.param("simple_template", "create_simple", {}),
            pytest.param(
                "with_optional_file_sections",
                "create_exclude_optional_file_sections",
                {},
            ),
            pytest.param(
                "with_optional_file_sections",
                "create_exclude_optional_file_sections",
                {"include_optional_field": False},
            ),
            pytest.param(
                "with_optional_file_sections",
                "create_include_optional_file_sections",
                {"include_optional_field": True},
            ),
            pytest.param(
                "with_optional_folders_files",
                "create_include_folders_files",
                {
                    "include_optional_files": True,
                    "include_optional_folder": True,
                    "creation_rules": {
                        "first/optional_folder": True,
                        "first/optional_folder/another_optional_file": True,
                        "second/optional_file.txt": True,
                    },
                },
            ),
            pytest.param(
                "with_optional_folders_files",
                "create_exclude_folders_include_files",
                {
                    "include_optional_files": True,
                    "include_optional_folder": False,
                    "creation_rules": {
                        "first/optional_folder": False,
                        "first/optional_folder/another_optional_file": True,
                        "second/optional_file.txt": True,
                    },
                },
            ),
            pytest.param(
                "with_optional_folders_files",
                "create_include_folders_exclude_files",
                {
                    "include_optional_files": False,
                    "include_optional_folder": True,
                    "creation_rules": {
                        "first/optional_folder": True,
                        "first/optional_folder/another_optional_file": False,
                        "second/optional_file.txt": False,
                    },
                },
            ),
            pytest.param(
                "with_optional_folders_files",
                "create_exclude_folders_exclude_files",
                {
                    "include_optional_files": False,
                    "include_optional_folder": False,
                    "creation_rules": {
                        "first/optional_folder": False,
                        "first/optional_folder/another_optional_file": False,
                        "second/optional_file.txt": False,
                    },
                },
            ),
            pytest.param(
                "with_custom_folder_and_file_paths",
                "create_with_custom_folder_and_file_paths",
                {
                    "target_file_name": "marge",
                    "target_folder_name": "homer",
                    "include_optional_target_folder_name": False,
                    "creation_rules": {
                        "{{target_folder_name}}/segment1/{{optional_target_folder_name}}": False  # noqa
                    },
                },
            ),
        ],
    )
    def test_create(self, template, expected, context):
        create_command = CreateCommand(
            template=template_folder(template), output=self._tmp_folder, context=context
        )
        self._use_case.execute(create_command)
        assert_folder(expected_folder(expected), self._tmp_folder)
