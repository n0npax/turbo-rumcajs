import os
import pytest


def pytest_generate_tests(metafunc):
    if 'testfile' in metafunc.fixturenames:
        return metafunc.parametrize("testfile", ['testfile_1.txt',
                                                 'testfile_2.dat',
                                                 'testfile_3'])


@pytest.fixture
def test_stuff_path():
    return os.path.dirname(__file__) + '/'


@pytest.fixture
def config_path(test_stuff_path):
    return test_stuff_path + 'test_config.cfg'
