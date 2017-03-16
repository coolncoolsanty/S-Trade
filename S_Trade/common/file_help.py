import os
import errno
import zipfile


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured


def unzip(zipfilename, unzipfolder):
    with zipfile.ZipFile(zipfilename, "r") as zip_ref:
        zip_ref.extractall(unzipfolder)
