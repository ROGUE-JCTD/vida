from django.conf import settings
from datetime import datetime
import os

# convert dict to object
class DictToObject(object):
    def __init__(self, d):
        self.__dict__['d'] = d

    def __getattr__(self, key):
        value = self.__dict__['d'][key]
        if type(value) == type({}):
            return DictToObject(value)
        return value

"""
example settings file
FILE_SERVICE_CONFIG = {
    'file_dir': '/webapps/vida/file_service_store'
}
"""
def get_file_service_dir():
    conf = getattr(settings, 'FILE_SERVICE_CONFIG', {})
    return conf.get('file_dir', './')


def u_to_str(string):
    return string.encode('ascii', 'ignore')


def is_int_str(v):
    v = str(v).strip()
    return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()


def add_file_attribs(target_object, filename):
    if os.path.isfile(filename):
        stat = os.stat(filename)
        if stat:
            target_object['file_size'] = stat.st_size
            target_object['file_updated'] = datetime.fromtimestamp(stat.st_ctime)


def get_file_service_files():
    return os.listdir(get_file_service_dir())


def file_exists(filename):
    if os.path.isfile(get_filename_absolute(filename)):
        return True
    return False


def get_filename_absolute(filename):
    return '{}/{}'.format(get_file_service_dir(), filename)
