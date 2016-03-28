from django.conf import settings
from datetime import datetime
import os
import logging
logger = logging.getLogger(__name__)

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
FILESERVICE_CONFIG = {
    'store_dir': '/webapps/vida/fileservice_store'
}
"""


def get_fileservice_dir():
    conf = getattr(settings, 'FILESERVICE_CONFIG', {})
    return conf.get('store_dir', './fileservice_store')


def get_fileservice_server_route_internal():
    conf = getattr(settings, 'FILESERVICE_CONFIG', {})
    return conf.get('server_route_internal', '/server_route_internal/')


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


def get_fileservice_files():
    return os.listdir(get_fileservice_dir())


def file_exists(filename):
    if os.path.isfile(get_filename_absolute(filename)):
        return True
    return False


def get_filename_absolute(filename):
    return '{}/{}'.format(get_fileservice_dir(), filename)


def get_gallery_file():
    conf = getattr(settings, 'FILESERVICE_CONFIG', {})
    return conf.get('gallery_file', get_fileservice_dir() + '/gallery.gal')


def get_fileservice_files_abs():
    result = []
    for i in get_fileservice_files():
        if 'thumb' in i:
            continue
        if i == "gallery.gal":
            continue
        logger.debug(i)
        result.append(get_filename_absolute(i))
    return result

