
from lib.py3rumcajs.helpers.file_processing import (validate_file,
                                                    validate_extension,
                                                    validate_by_regex,
                                                    remove_duplicates,
                                                    )



def test_validate_file(testfile, test_stuff_path):
    filepath = test_stuff_path + testfile


def test_validate_file_extension(testfile, test_stuff_path):
    filepath = test_stuff_path + testfile
    assert validate_extension(filepath) == True


def test_validate_file_by_regex(testfile, test_stuff_path):
    pass


def test_remove_duplicates(testfile, test_stuff_path):
    pass
