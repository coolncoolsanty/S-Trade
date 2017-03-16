from common.db_connection import DbEngine


class DBConfig(object):
    def __init__(self, config_class):
        """
        :param config_class: Name of the config class under the configurations

        """

        self._dict = {}
        self._db_engine = DbEngine()
        self._conn = self._db_engine.get_connection()

        self._query = "call sp_getconfig('{0}')".format(config_class)

        self._result = self._conn.execute(self._query)

        for self._row in self._result:
            if self._row['key'] in self._dict.keys():
                if isinstance(self._dict[self._row['key']], (list, tuple)):
                    self._dict[self._row['key']].append(self._row['value'])
                else:
                    temp = self._dict[self._row['key']]
                    self._dict[self._row['key']] = [temp, self._row['value']]
            else:
                self._dict[self._row['key']] = self._row['value']
        self._conn.close()

    def get_value(self, key, default_value=None):
        """
        :param self:            Reference to itself as a instance of this class
        :param key:            The dictionary key
        :param default_value:    Default - None otherwise user defined value
        :returns:               One of None, user defined value or instance member's
                                dictionary value for the given key
        """
        try:
            return self._dict[key]
        except KeyError:
            return default_value


def _process_main(config_class='etl'):
    """ This method does the core processing for this script

    :param config_class:  the config class for which the key values pair dictionary is
                            expected from the db config
    :returns:           0 : Success, 1: Failure
    """

    try:
        c_dict = DBConfig(config_class=config_class)
        if c_dict:
            print(c_dict)
            print(c_dict.get_value('root'))
            print(c_dict.get_value('source'))
            print(c_dict.get_value('source')[2])
            print(c_dict.get_value('source')[1])
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
