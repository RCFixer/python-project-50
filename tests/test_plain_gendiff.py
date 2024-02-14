import os

import pytest

from gendiff.scripts.gendiff import generate_diff


@pytest.fixture
def expected_result():
    return '''Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]'''


def test_first_case(expected_result):
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    file1 = os.path.join(current_dir_path, 'fixtures/rec_file1.json')
    file2 = os.path.join(current_dir_path, 'fixtures/rec_file2.json')
    result = generate_diff(file1, file2, 'plain')
    assert result == expected_result


def test_yaml_case(expected_result):
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    file1 = os.path.join(current_dir_path, 'fixtures/rec_file1.yaml')
    file2 = os.path.join(current_dir_path, 'fixtures/rec_file2.yaml')
    result = generate_diff(file1, file2, 'plain')
    assert result == expected_result
