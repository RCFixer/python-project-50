import os
import json

import pytest

from gendiff.scripts import generate_diff


@pytest.fixture
def expected_result():
    return json.dumps({"  common": {"+ follow": False, "  setting1": "Value 1", "- setting2": 200, "- setting3": True,
                         "+ setting3": None, "+ setting4": "blah blah", "+ setting5": {"key5": "value5"},
                         "  setting6": {"  doge": {"- wow": "", "+ wow": "so much"},
                                        "  key": "value", "+ ops": "vops"}},
            "  group1": {"- baz": "bas", "+ baz": "bars", "  foo": "bar", "- nest": {"key": "value"},
                         "+ nest": "str"}, "- group2": {"abc": 12345, "deep": {"id": 45}},
            "+ group3": {"deep": {"id": {"number": 45}}, "fee": 100500}})



def test_first_case(expected_result):
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    file1 = os.path.join(current_dir_path, 'fixtures/rec_file1.json')
    file2 = os.path.join(current_dir_path, 'fixtures/rec_file2.json')
    result = generate_diff(file1, file2, 'json')
    assert result == expected_result


def test_yaml_case(expected_result):
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    file1 = os.path.join(current_dir_path, 'fixtures/rec_file1.yaml')
    file2 = os.path.join(current_dir_path, 'fixtures/rec_file2.yaml')
    result = generate_diff(file1, file2, 'json')
    assert result == expected_result
