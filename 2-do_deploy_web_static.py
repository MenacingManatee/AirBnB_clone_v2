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

def do_deploy(archive_path):
    '''Deploys archive to webserver'''
    from fabric.api import env
    if not os.path.exists(archive_path):
        return False
    env.hosts = ['34.73.196.89', '54.221.178.230']
    env.user = 'ubuntu'
    env.key_filename = '~/.ssh/holberton'
    a_name = archive_path.split('/')[-1]
    d_name = a_name.split('.')[0]
    dwr = "/data/web_static/releases/"
    success = []
    tmp = put(archive_path, '/tmp/' + a_name + '/')
    success.append(tmp.succeeded)
    tmp = run("mkdir -p " + dwr + d_name + '/')
    success.append(tmp.succeeded)
    tmp = run("tar -xzf /tmp/" + a_name + " -C " + dwr + d_name + '/')
    success.append(tmp.succeeded)
    tmp = run("rm /tmp/" + a_name)
    success.append(tmp.succeeded)
    tmp = run("mv " + dwr + d_name + "/web_static/* " + dwr + d_name + '/')
    success.append(tmp.succeeded)
    tmp = run("rm -rf " + dwr + d_name + '/web_static')
    success.append(tmp.succeeded)
    tmp = run("rm -rf /data/web_static/current")
    success.append(tmp.succeeded)
    tmp = run("ln -s " + dwr + d_name + '/ /data/web_static/current')
    success.append(tmp.succeeded)
    if False in success:
        return False
    return True
    
