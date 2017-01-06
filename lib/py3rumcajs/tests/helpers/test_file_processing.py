import pytest

from werkzeug.datastructures import FileStorage
from lib.py3rumcajs.helpers.file_processing import (validate_file,
                                                    validate_extension,
                                                    validate_by_1stline,
                                                    parse_to_dict,
                                                    )


def test_validate_file(testfile, test_stuff_path):
    filepath = test_stuff_path + testfile
    with open(filepath, 'r') as fp:
        file = FileStorage(fp)
        assert validate_file(file) == True


def test_validate_file_extension(testfile, test_stuff_path):
    filepath = test_stuff_path + testfile
    with open(filepath, 'r') as fp:
        file = FileStorage(fp)
        assert validate_extension(file) == True


def test_validate_by1stline(testfile, test_stuff_path):
    filepath = test_stuff_path + testfile
    with open(filepath, 'r') as fp:
        file = FileStorage(fp)
        assert validate_by_1stline(file) == True


def test_validate_file_by_regex_fail(fail_testfile, test_stuff_path):
    filepath = test_stuff_path + fail_testfile
    with open(filepath, 'r') as fp:
        file = FileStorage(fp)
        assert validate_file(file) == False


def test_parse(testfile, test_stuff_path):
    data = parse_to_dict(testfile)
    assert data['data'] != []
    assert data['name'] == testfile
    assert type(data['y_prefix']) == str
    assert type(data['x_prefix']) == str


@pytest.mark.skip(reason="no implemented feture yet")
def test_rescale_data():
    raise
