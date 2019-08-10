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
    _assert_folder(expected_folder, actual_folder)
    _assert_folder(actual_folder, expected_folder)


def _assert_folder(lhs_folder, rhs_folder):
    assert os.path.isdir(rhs_folder), rhs_folder
    for name in os.listdir(rhs_folder):
        rhs_path = os.path.join(rhs_folder, name)
        lhs_path = os.path.join(lhs_folder, name)

        if os.path.isdir(rhs_path):
            os.path.isdir(lhs_path)
            _assert_folder(
                lhs_folder=os.path.join(lhs_path), rhs_folder=os.path.join(rhs_path)
            )
        elif os.path.isfile(rhs_path):
            assert os.path.isfile(lhs_path), lhs_path
            _assert_file(lhs_path, rhs_path)


def _assert_file(lhs_file, rhs_file):
    lhs_contents = open(lhs_file).read()
    rhs_contents = open(rhs_file).read()

    if lhs_contents != rhs_contents:
        diffs = [
            line
            for line in context_diff(
                lhs_contents, rhs_contents, fromfile=lhs_file, tofile=rhs_file
            )
        ]

        assert False, "".join(diffs)


def tmp_folder():
    substring = "".join(random.choice(string.ascii_letters) for _ in range(6))
    folder = f"/tmp/{substring}"
    os.makedirs(folder)
    return folder
