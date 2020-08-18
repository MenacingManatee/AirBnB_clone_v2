#!/usr/bin/python3
'''generates a .tgz archive from the contents of the web_static folder'''
from fabric.operations import local
from datetime import datetime
import os


def do_pack():
    '''Packs web_static'''
    tmp = datetime.utcnow()
    tmp = tmp.strftime("%Y%m%d%T%H%M%S").replace(':', '')
    try:
        os.mkdir("./versions")
    except FileExistsError:
        pass
    local("tar -czvf versions/web_static_" + tmp + ".tgz web_static")
