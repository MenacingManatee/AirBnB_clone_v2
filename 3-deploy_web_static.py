#!/usr/bin/python3
'''generates a .tgz archive from the contents of the web_static folder'''
from fabric.api import local, env, run, put
from datetime import datetime
import os


def do_pack():
    '''Packs web_static'''
    tmp = datetime.utcnow()
    tmp = tmp.strftime("%Y%m%d%T%H%M%S").replace(':', '')
    try:
        os.mkdir("./versions")
    except:
        pass
    tmp2 = local("tar -czvf versions/web_static_" + tmp + ".tgz web_static")
    return [tmp2.succeeded, tmp]


env.hosts = ['34.73.196.89', '54.221.178.230']


def do_deploy(archive_path):
    '''Deploys archive to webserver'''
    if not os.path.exists(archive_path):
        return False
    a_name = archive_path.split('/')[-1]
    d_name = a_name.split('.')[0]
    dwr = "/data/web_static/releases/"

    put(archive_path, '/tmp/')
    run("mkdir -p " + dwr + d_name + '/')
    run("tar -xzf /tmp/" + a_name + " -C " + dwr + d_name + '/')
    run("rm /tmp/" + a_name)
    run("mv " + dwr + d_name + "/web_static/* " + dwr + d_name + '/')
    run("rm -rf " + dwr + d_name + '/web_static')
    run("rm -rf /data/web_static/current")
    run("ln -s " + dwr + d_name + '/ /data/web_static/current')
    return True


def deploy():
    '''creates and distributes an archive to your web servers'''
    pack = do_pack()
    if pack[0] == False:
        return False
    return do_deploy('versions/' + pack[1])
