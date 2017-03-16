from common.parse_ini_config import ParseConfig
from sqlalchemy import create_engine
import pymysql


class DbEngine(object):
    def __init__(self, section='db_default'):
        """
        This object to get all the related data to initiate the database connection
        :param section: name of the database this entry should be present in the configs
        """

        self._conf = ParseConfig(section=section)

        self._host = self._conf.get_value('host')
        self._port = self._conf.get_value('port')
        self._username = self._conf.get_value('username')
        self._password = self._conf.get_value('password')
        self._db = self._conf.get_value('db')

        self._engine = None

    def get_connection(self):
        try:
            '''
            returns db engine object
            '''
            self._engine = create_engine(
                "mysql+pymysql://{0}:{1}@{2}/{3}?{4}?port={5}".format(
                    self._username, self._password, self._host, self._db, self._host, self._port))

        except Exception as e:
            print('Unable to create connection' + str(e))
            exit()
        return self._engine.connect()
