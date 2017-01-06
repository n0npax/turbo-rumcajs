import pytest

import lib.py3rumcajs.app_config.config


class TestConfig:

    def test_get_value_list(self, config_path):

        config = lib.py3rumcajs.app_config.config.Config(config_path)
        for extension in config.file.extensions:
            assert extension in ['.txt', '.data', '.dat', '']

    def test_get_value(self, config_path):

        config = lib.py3rumcajs.app_config.config.Config(config_path)
        assert config.log.level == 'DEBUG'

    def test_get_fake_value(self, config_path):

        config = lib.py3rumcajs.app_config.config.Config(config_path)
        with pytest.raises(AttributeError):
            config.log.wrong_key

    def test_get_fake_section(self, config_path):

        config = lib.py3rumcajs.app_config.config.Config(config_path)
        with pytest.raises(AttributeError):
            config.wrong_section
