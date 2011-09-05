import os
from datetime import datetime

from fabric.api import *
from fabric.decorators import runs_once
from fabric.contrib.files import exists
from fabric import utils

### SET ME ###
env.key_filename = '' # set me. full path to where your AWS key file is located.
env.hosts = [''] # Fill me in with URLs to your instance(s).

env.user = "ubuntu"
env.project = "lolaws"
env.project_code_name = "lolaws"
env.wsgi_file = 'lolaws.wsgi'

env.settings_name = "settings"
env.root = '/home/lolaws/lolaws'
env.dev_root = '/home/lolaws/lolaws/'

env.code_root = os.path.join(env.dev_root, env.project_code_name)
env.code_pack_location = os.path.join('/tmp/', '{0}.tar.gz'.format(env.project))
env.virtual_env_home = '/home/lolaws/env/'.format(env.project, env.project)

def run_in_virtualenv(command):
    """
    Special helper function to run remote commands in virtual env. Just appends
    the virtualenv activate on to the front of the command. This has to be
    called for _each_ remote command requiring virtualenv because the virtualenv
    activation doesn't persist, the same way 'cd' doesn't.

    """
    activate_command = '. {0}/activate'.format(os.path.join(env.virtual_env_home, 'bin'))
    sudo('{0}; {1}'.format(activate_command, command))

@runs_once
def killpyc():
    """ Delete .pyc files """
    #local("rm -rf *.pyc")
    local("find . -name \"*.pyc\" -delete")

def clean_local():
    """ Delete archive from past deployment if it exists. """
    if os.path.isfile('/{0}.tar.gz'.format(env.project)):
        local('rm /{0}.tar.gz'.format(env.project))

@runs_once
def clean_remote():
    """ Delete code on remote server. """
    if exists(env.code_root, verbose=True):
        # ugh... scary to do -rm * on an coded dir
        sudo('rm -rf {0}'.format(os.path.join(env.code_root, '*')))

def clean_remote_pack():
    if exists(env.code_pack_location, verbose=True):
        sudo('rm {0}'.format(env.code_pack_location))

def pack():
    """ Pack up project git repo into an archive. """
    clean_local()
    killpyc()
    # awful hack
    if not os.path.isfile('./fabfile.py'):
        utils.abort('Please run this from the root of the project (miscasa/.)')
    local('cd ../; tar -pczf /{0}.tar.gz .'.format(env.project, env.dev_root))
#    local('cd ../; git archive HEAD --format=tar | gzip > {0}.tar.gz'.format(env.project)) #lolaws.tar.gz

def transfer():
    """ Send code archive to server for deployment. """
    if not os.path.isfile('/{0}.tar.gz'.format(env.project)):
        utils.abort('Could not find code archive to send to server.')
    put('/{0}.tar.gz'.format(env.project), '/tmp/')
    clean_local()

def unpack():
    """ Untar's code archive on the remote machine. """
    clean_remote()
    if exists(env.code_pack_location):
        with cd(env.dev_root):
            sudo('tar xf {0}'.format(env.code_pack_location))

def clean_remote_pack():
    """ activate VM and run collectstatic """
    run_in_virtualenv("cd {0}; python manage.py collectstatic --noinput --link --settings={1}".format(env.code_root, env.settings_name))

def install_requirements():
    """ Install requirements """
    with cd(env.dev_root):
        run_in_virtualenv("pip install -r requirements.txt")

def restart_webserver():
    """ Restarts Apache."""
    sudo('/etc/init.d/apache2 restart')

def touch_wsgi():
    """ Touches the wsgi file, causing app to reload. """
    apache_dir = os.path.join(env.code_root, 'apache')
    with cd(apache_dir):
        sudo('touch {0}'.format(env.wsgi_file))

def setup():
    if not exists(env.root):
        sudo('mkdir {0}'.format(env.root))

    if not exists(env.code_root):
        sudo('mkdir {0}'.format(env.code_root))

def syncdb():
    """ Run Django syncdb on remote maachine. """
    with cd(env.code_root):
        run_in_virtualenv('python manage.py syncdb')

def collectstatic():
    with cd(env.code_root):
            run_in_virtualenv("python manage.py collectstatic --noinput --link --settings={0}".format(env.settings_name))


def deploy():
    """ Deploys new code to boxes in env.hosts. """
    setup()
    pack()
    transfer()
    unpack()
    install_requirements()
    touch_wsgi()
