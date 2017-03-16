import datetime
import requests
import shutil
from common.db_config import DBConfig
from common import str_help, date_help, file_help
import stat
import os
import pandas as pd


class NSEBhavcopyWeb(object):

    def __init__(self):
        self._c_dict = DBConfig(config_class='etl.nse.nseweb.bhavcopy')

    def _download_bhavcopy(self, ddate=None):

        _root_path = self._c_dict.get_value('root')
        _folder = self._c_dict.get_value('path')
        _bhavcopy_folder = _root_path + _folder
        _bhavcopy_zipfileName = 'cm' + ddate.strftime('%d%b%Y').upper() + 'bhav.csv.zip'
        _bhavcopy_zipfilePath = _root_path + _folder + _bhavcopy_zipfileName

        os.makedirs(_bhavcopy_folder, exist_ok=True)
        os.chmod(_bhavcopy_folder, stat.S_IRWXO)

        # sample link - 'https://www.nseindia.com/content/historical/EQUITIES/2017/JAN/cm03JAN2017bhav.csv.zip'
        _bhavcopy_url = self._c_dict.get_value('url')
        _bhavcopy_url = str_help.str_replace_date(_bhavcopy_url, ddate)

        print('url - ', _bhavcopy_url)
        file_help.silent_remove(_bhavcopy_zipfilePath)
        _r = requests.get(_bhavcopy_url, stream=True)
        # print(r.status_code)
        if _r.status_code == 200:
            with open(_bhavcopy_zipfilePath, 'wb') as f:
                _r.raw.decode_content = True
                shutil.copyfileobj(_r.raw, f)
        else:
            return 'Fail', _bhavcopy_url, None, 'url return code - '+str(_r.status_code)

        _bhavcopy_csvFile = None
        if os.path.isfile(_bhavcopy_zipfilePath):
            _bhavcopy_csvdir = _bhavcopy_zipfilePath.replace('.csv.zip', '')

            file_help.unzip(_bhavcopy_zipfilePath, _bhavcopy_csvdir)

            _bhavcopy_csvFileName = 'cm' + ddate.strftime('%d%b%Y').upper() + 'bhav.csv'
            _bhavcopy_csvFile = _bhavcopy_csvdir + '\\' + _bhavcopy_csvFileName

            file_help.silent_remove(_bhavcopy_folder + '\\' + _bhavcopy_csvFileName)
            shutil.move(_bhavcopy_csvFile, _bhavcopy_folder + '\\' + _bhavcopy_csvFileName)

            _bhavcopy_csvFile = _bhavcopy_folder + '\\' + _bhavcopy_csvFileName

            shutil.rmtree(_bhavcopy_csvdir)
            file_help.silent_remove(_bhavcopy_zipfilePath)

            print(_bhavcopy_csvFile)
        return 'Success', _bhavcopy_url, _bhavcopy_csvFile, ''

    def extract_bhavcopy(self, ddate=None):
        if ddate is None:
            ddate = datetime.date.today()

        if date_help.check_weekday(ddate) in [0, 6]:
            return 'Fail', None, None, 'Holiday'

        _status, _bhavcopy_url, _bhavcopy_csvfile, _remarks = self._download_bhavcopy(ddate)

        if _status == 'Success':
            _bhavcopy_df = pd.read_csv(_bhavcopy_csvfile)
            return 'Success', _bhavcopy_df, _bhavcopy_url, 'Download Success'
        else:
            return 'Fail', None, _bhavcopy_url, _remarks

    """
        def _download_bhavcopy_range(self, from_date=None, to_date=None):
        if from_date is None:
            min_date = self._c_dict.get_value('min_date')
            from_date = datetime.datetime.strptime(min_date, '%Y-%m-%d')
        if to_date is None:
            to_date = datetime.datetime.today()

        for date in date_help.datetime_range(from_date, to_date):
            print('downloading for date - ', date)
            filepath = self.download_bhavcopy(date)
            print('return - ', filepath)
    """


def main():
    loader = NSEBhavcopyWeb()
    # loader.download_bhavcopy_range()
    # loader.download_bhavcopy_range(from_date=datetime.datetime(2017, 3, 1), to_date=datetime.datetime(2017, 3, 15))
    # loader.download_bhavcopy_range(datetime.datetime.today(), datetime.datetime.today())
    print(loader.extract_bhavcopy(datetime.datetime(2017, 3, 13)))

# main()
