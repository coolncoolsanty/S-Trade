import configparser
import common
import os

class ParseConfig(object):
    def __init__(self, section):
        """
        This object is used to read the configuration file and create a dictionary
        :param self:            Reference to itself as a instance of this class
        :param section:         the section in the config to be accessed
        """

        self.config = configparser.ConfigParser()

        self.config.read(os.path.dirname(common.__file__)+'\db_connstring.ini')

        self._config_dict = self._as_dict()

        self._dict = self._config_dict[section]

    def _as_dict(self):
        """
        Converts a ConfigParser object into a dictionary.

        The resulting dictionary has sections as keys which point to a dict of the
        sections options as key => value pairs.
        """
        the_dict = {}
        for section in self.config.sections():
            the_dict[section] = {}
            for key, val in self.config.items(section):
                the_dict[section][key] = val
        # print(the_dict)
        return the_dict

    def get_value(self, name, default_value=None):
        """
        :param self:            Reference to itself as a instance of this class
        :param name:            The dictionary key
        :param default_value:    Default - None otherwise user defined value
        :returns:               One of None, user defined value or instance member's
                                dictionary value for the given key
        """
        try:
            return self._dict[name]
        except KeyError:
            return default_value


def _process_main(section='db_default'):
    """ This method does the core processing for this script

    :param section:  defines the section to be scanned
    :returns:           0 : Success, 1: Failure
    """
    try:
        config = ParseConfig(section=section)
        if config:
            print(config.get_value('host'))
            return 1
        else:
            return 0
    except Exception as e:
        print(str(e))
        return 0


def main():
    status = _process_main()
    print(status)

# main()
