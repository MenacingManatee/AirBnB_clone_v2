#!/usr/bin/python3
'''deploys a .tgz archive to a web server'''
from fabric.api import env, put, run
from datetime import datetime
import os


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
    
