import os

import pytest

from gendiff.scripts import generate_diff


@pytest.fixture
def expected_result():
    return '{\n\t- follow: false\n\t  host: hexlet.io\n\t- proxy:' \
           ' 123.234.53.22\n\t- timeout: 50\n\t+ timeout: 20\n\t+ verbose: true\n}'


def test_first_case(expected_result):
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    file1 = os.path.join(current_dir_path, 'fixtures/file1.json')
    file2 = os.path.join(current_dir_path, 'fixtures/file2.json')
    result = generate_diff(file1, file2)
    assert result == expected_result