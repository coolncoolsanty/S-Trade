from etl.extract_nse_bhavcopy_web import NSEBhavcopyWeb
from common.db_config import DBConfig
from common.db_connection import DbEngine
import datetime


class NSEWrapper(object):

    def __init__(self):
        self._c_dict = DBConfig(config_class='etl')

    def bhavcopy_etl(self, d_date=None):

        if d_date is None:
            # get max date from database
            _db_engine = DbEngine()
            _conn = _db_engine.get_connection()
            _query = "select COALESCE(max(date), STR_TO_DATE('1994-11-07','%%Y-%%m-%%d')) max_date \
                     from tbl_log_etl where filetype = 'BhavCopy'"
            _result = _conn.execute(_query)
            d_date = _result.fetchone()[0]

        extractor = NSEBhavcopyWeb()
        print(extractor.extract_bhavcopy(d_date))


def main():
    loader = NSEWrapper()
    print(loader.bhavcopy_etl(datetime.datetime(2017, 3, 13)))

main()
