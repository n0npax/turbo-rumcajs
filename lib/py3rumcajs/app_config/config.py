import configparser


class Config(object):

    class Section(object):

        def __init__(self, section):
            self.section = section

        def __getattr__(self, name):
            if name in self.section:
                values = self.section[name].split('\n')
                if len(values) == 1:
                    return values[0]
                else:
                    return [value.strip() for value in values]
            raise AttributeError

    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def __getattr__(self, name):
        if name in self.config:
            return Config.Section(self.config[name])
        else:
            raise AttributeError
