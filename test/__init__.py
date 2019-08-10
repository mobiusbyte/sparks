import os
import random
import string
from difflib import context_diff


def fixture_path(name):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "fixtures", name)


def template_folder(template_name):
    return os.path.join(fixture_path("templates"), template_name)


def expected_folder(test_case):
    return os.path.join(fixture_path("expectations"), test_case)


def assert_folder(expected_folder, actual_folder):
    assert os.path.isdir(actual_folder), actual_folder
    for name in os.listdir(actual_folder):
        actual_path = os.path.join(actual_folder, name)
        expected_path = os.path.join(expected_folder, name)

        if os.path.isdir(actual_path):
            os.path.isdir(expected_path)
            assert_folder(
                expected_folder=os.path.join(expected_path),
                actual_folder=os.path.join(actual_path),
            )
        elif os.path.isfile(actual_path):
            assert os.path.isfile(expected_path), expected_path
            _assert_file(expected_path, actual_path)


def _assert_file(expected, actual):
    actual_contents = open(actual).read()
    expected_contents = open(expected).read()

    if expected_contents != actual_contents:
        diffs = [
            line
            for line in context_diff(
                expected_contents, actual_contents, fromfile=expected, tofile=actual
            )
        ]

        assert False, "".join(diffs)


def tmp_folder():
    substring = "".join(random.choice(string.ascii_letters) for _ in range(6))
    folder = f"/tmp/{substring}"
    os.makedirs(folder)
    return folder
