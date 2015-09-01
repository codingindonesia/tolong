import os

from fabric.api import env, run, local, sudo, prompt
from fabric.context_managers import cd, settings
from fabric.contrib.files import exists, upload_template
from fabric.utils import abort

from db import create_db
from migrations import migrate, check_migration_type
from webservers import setup_webserver, restart_webserver

from fabtools import require


def setup_env(target_dir='tolong'):
    env.PROJECT_NAME = target_dir
    env.PROJECT_PATH = '/var/www/%s/' % env.PROJECT_NAME
    env.SRC_PATH = os.path.join(env.PROJECT_PATH, 'src')
    env.TEMP_SRC_PATH = os.path.join(env.PROJECT_PATH, 'temp')
    env.VIRTUALENV_DIR = os.path.join(env.PROJECT_PATH, 'env')
    env.PYTHON_BIN = os.path.join(env.VIRTUALENV_DIR, 'bin/python')
    env.PIP_BIN = os.path.join(env.VIRTUALENV_DIR, 'bin/pip')
    env.REQUIREMENTS_FILE = os.path.join(env.SRC_PATH, "requirements.txt")
    env.MANAGE_PATH = os.path.join(env.SRC_PATH, 'manage.py')
    env.MANAGE_BIN = '{0} {1}'.format(env.PYTHON_BIN, env.MANAGE_PATH)


def install_project_requirements(path_to_file=None):
    path_to_file = path_to_file or env.REQUIREMENTS_FILE
    if exists(path_to_file):
        sudo('{0} install -r {1}'.format(env.PIP_BIN, path_to_file))


def create_deployment_key():
    """
    Create a private key for deployment purposes in /var/www/.ssh
    """
    if not exists(env.DEPLOYMENT_KEY):
        require.users.user(name='www-data')
        require.files.directory('/var/www/.ssh', use_sudo=True,
                                owner='www-data', group='www-data')
        sudo('ssh-keygen -f {0}'.format(env.DEPLOYMENT_KEY), user='www-data')


def deploy_project(target_dir='tolong'):
    """ Deploys a project for the first time """
    setup_env(target_dir)

    if exists("%s" % env.PROJECT_PATH):
        abort('Project already deployed. Run "fab update_project -H <host>" instead')

    setup_os()
    require.files.directory(env.PROJECT_PATH, use_sudo=True,
                            owner='www-data', group='www-data')
    update_source_code(deploy=True)
    setup_virtualenv()
    log_dir = os.path.join(env.PROJECT_PATH, 'logs')
    require.files.directory(log_dir, use_sudo=True,
                            owner='www-data', group='www-data')
    setup_webserver()
    create_db()
    context = {
        'db_name': env.db_name,
        'db_user': env.db_user,
        'db_pass': env.db_pass,
    }
    upload_template('fabfiles/conf_templates/settings_local.py.tpl',
                    env.HOME_PATH, context=context)
    sudo('mv %ssettings_local.py.tpl %s/%s/settings_local.py' %
         (env.HOME_PATH, env.SRC_PATH, env.PROJECT_NAME))
    install_project_requirements()
    collect_static()
    # compress_static()
    sudo('chown -R www-data:www-data %s' % env.PROJECT_PATH)
    sudo('{0} syncdb'.format(env.MANAGE_BIN))
    migrate()
    '''
    print("""Finished deployment. Now you need to:\n
      1. Edit your %s/settings_local.py file\n
      2. Run "fab create_initial_migration -H <host>"\n
      3. Connect to server and run "%s manage.py syncdb" from %ssrc\n
      4. Run "fab migrate -H <host>"\n
      5. Run "fab collect_static -H <host>" """ %
        (env.SRC_PATH, env.PYTHON_BIN, env.PROJECT_PATH))
    '''
    restart_webserver()


def collect_static():
    """ Runs django.contrib.staticfiles collectstatic command"""
    sudo('{0} collectstatic -l --noinput'.format(env.MANAGE_BIN), user='www-data')


def check_django_shell():
    output = sudo('ps aux | grep "manage.py shell" | grep -v grep | awk \'{ print $1" "$11" "$12" "$13}\'')
    if output:
        abort("""There is one or more django shell running on the system, please kill them first""")


def run_test():
    """
    Test application for error before deploying, abort deployment on failing test
    """
    local("python manage.py test --failfast")


def update_project(skip_test="true", target_dir='tolong'):
    """ Updates the source directory with most recent code, create migration
    and then restarts the webserver """
    setup_env(target_dir)
    if skip_test != "true":
        run_test()

    check_django_shell()

    # update temporary source code first, so we can know whether migration has addition
    # or deletion
    update_source_code(path=env.TEMP_SRC_PATH)
    symlink_settings_local()
    install_project_requirements(os.path.join(env.TEMP_SRC_PATH, 'requirements.txt'))

    migration_type = check_migration_type()
    if migration_type == "update_source_then_migrate":
        update_source_code()
        collect_static()
        # compress_static()
        restart_webserver()
        migrate()
        return
    elif migration_type == "migrate_then_update_source":
        # Migrate from temporary first
        migrate(env.TEMP_SRC_PATH)
        #  then normal stuff without migration again
        update_source_code()
    elif migration_type is None:
        update_source_code()

    collect_static()
    # compress_static()
    restart_webserver()


def compress_static():
    """ Runs django_compressor's compress command"""
    with cd(env.SRC_PATH):
        sudo('{0} compress --force'.format(env.MANAGE_BIN), user='www-data')


def setup_os():
    """ Prepare OS with necessary packages to host a django project """
    require.deb.packages([
        'python-setuptools',
        'python-dev',
        'build-essential',
        'libjpeg-dev',
        'python-imaging',
        'git-core',
        'libmysqlclient-dev',
        'libpq-dev',
        'python-mysqldb',
        'python-pylibmc',
        'python-lxml',
        'memcached',
        'libmemcached-dev',
        'libxml2-dev',
        'libxslt-dev',
        'gdal-bin',
    ])
    require.python.packages(['fabtools', 'pip'], use_sudo=True)


def update_source_code(path=None, deploy=False):
    """ Update project's source dir from git repo"""
    # If no repo is present, clone from localhost
    path = env.SRC_PATH if path is None else path

    if not exists(path):
        # Make a new deployment key if not already there
        if not exists(env.DEPLOYMENT_KEY, use_sudo=True):
            create_deployment_key()
        if deploy:
            git_cmd = 'git clone git@github.com:codingindonesia/tolong.git {0}'.format(path)
        else:
            git_cmd = 'cd {0} && git pull'.format(path)
        require.files.directory(env.PROJECT_PATH, use_sudo=True)
        sudo('chown -R www-data {0}'.format(env.PROJECT_PATH))
        with cd(env.PROJECT_PATH):
            with settings(warn_only=True):
                result = sudo(git_cmd, user='www-data')
            if result.failed:
                abort("""Failed to clone git repository. Make sure that root
                    is allowed to clone repository by running this
                    on the server:
                    sudo -u www-data git clone git@github.com:codingindonesia/tolong.git""".format(env.REPO_NAME))

    # Get current git hash on the local machine
    git_hash = local('git rev-parse HEAD', capture=True)
    with cd(path):
        sudo('git fetch', user='www-data')
        sudo('git checkout {0}'.format(git_hash), user='www-data')
    if path == env.SRC_PATH:
        with cd(env.PROJECT_PATH):
            sudo('echo "{0}:{1}:{2}" >> revisions.log'.format(env.TIME, git_hash, env.user))


def setup_virtualenv():
    """ Setup virtualenv for a project """
    require.python.package('virtualenv', use_sudo=True)
    django_version = prompt('Django version to install [None]:')
    with cd(env.PROJECT_PATH):
        sudo('virtualenv env --system-site-packages')
    install_cmd = '{0} install -U django'.format(env.PIP_BIN)
    if django_version:
        install_cmd = install_cmd + '=={0}'.format(django_version)
    sudo(install_cmd)
    # sudo('{0} install -U south'.format(env.PIP_BIN))


def cleanup_removed_directories():
    dirs = run(
        '%s %s/fabfiles/scripts/get_dirs_to_remove.py --source_dir=%s%s --target_dir=%s --exclude=migrations,static' %
            (env.PYTHON_BIN, env.SRC_PATH, env.HOME_PATH, env.PROJECT_NAME,
             env.SRC_PATH))

    dirs = sorted(dirs.strip().split())
    for directory in dirs:
        if exists(directory):
            answer = prompt('Sure you want to delete %s [y/N]?' % directory)
            if answer == 'y':
                sudo('rm -r %s' % directory)


def symlink_settings_local():
    temp_settings_local = os.path.join(env.TEMP_SRC_PATH, 'childsos', "settings_local.py")
    if not exists(temp_settings_local):
        main_settings_local = os.path.join(env.SRC_PATH, 'childsos', "settings_local.py")
        sudo('ln -s {0} {1}'.format(main_settings_local, temp_settings_local), user='www-data')
