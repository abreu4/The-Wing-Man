import os
from hashlib import md5


def filenumber(element):

    """ Given relative filepath, returns integer in file's name """

    return int(os.path.splitext(element)[0])


def file_hash(filepath):

    """ Given filepath, generates unique md5 hash """

    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()
