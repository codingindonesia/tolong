from __future__ import with_statement
from fabric.api import env, local, prompt, get
from time import strftime

from fabfiles.db import *
from fabfiles.deploy import *
from fabfiles.migrations import *
from fabfiles.webservers import *


env.PROJECT_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__))).lower()
env.PROJECT_PATH = '/var/www/%s/' % env.PROJECT_NAME
env.HOME_PATH = ('/home/%s/' % env.user)
env.TIME = strftime("%Y-%m-%d_%H:%M")
env.SRC_PATH = os.path.join(env.PROJECT_PATH, 'src')
env.TEMP_SRC_PATH = os.path.join(env.PROJECT_PATH, 'temp')
env.REPO_NAME = 'tolong'
env.GIT_PATH = '/srv/git/repositories/{0}.git'.format(env.REPO_NAME)
env.VIRTUALENV_DIR = os.path.join(env.PROJECT_PATH, 'env')
env.PYTHON_BIN = os.path.join(env.VIRTUALENV_DIR, 'bin/python')
env.PIP_BIN = os.path.join(env.VIRTUALENV_DIR, 'bin/pip')
env.REQUIREMENTS_FILE = os.path.join(env.SRC_PATH, "requirements.txt")
env.DEPLOYMENT_KEY = '/var/www/.ssh/id_rsa'
env.MANAGE_PATH = os.path.join(env.SRC_PATH, 'manage.py')
env.MANAGE_BIN = '{0} {1}'.format(env.PYTHON_BIN, env.MANAGE_PATH)
