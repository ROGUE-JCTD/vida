from vida.settings.local_settings import LOCAL_HOST_IP

def is_int_str(v):
    v = str(v).strip()
    return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()

def get_network_ip():
    return LOCAL_HOST_IP