from fabric.api import env, sudo, prompt
from fabric.context_managers import cd
from fabric.contrib.files import upload_template


def setup_webserver():
    """ Setups nginx or Apache """
    """
    string = 'Webserver\n1. Apache mod_wsgi\n2. NginX + gunicorn:'
    webserver = int(prompt(string, 'webserver'))
    if webserver not in [1, 2]:
        abort("You must enter 1 or 2")
    elif webserver == 1:
        setup_apache()
        restart_apache()
    """
    setup_apache()
    restart_apache()


def setup_apache(template='apache.conf.tpl'):
    """ Setup apache with mod_wsgi to run django """
    sudo('apt-get install libapache2-mod-wsgi')
    server_name = prompt('Enter server name (e.g example.com):', 'server_name')
    upload_template(
        'fabfiles/conf_templates/%s' % template, env.HOME_PATH,
        context={
            'server_name': server_name,
            'project_path': env.PROJECT_PATH,
            'project_name': env.PROJECT_NAME,
        }
    )
    sudo('mv %s /etc/apache2/sites-available/%s.conf' % (template, env.PROJECT_NAME))
    sudo('ln -s /etc/apache2/sites-available/%s.conf /etc/apache2/sites-enabled/%s.conf' %
         (env.PROJECT_NAME, env.PROJECT_NAME))
    sudo('a2ensite %s' % env.PROJECT_NAME)


def restart_webserver():
    """ Restarts gunicorn"""
    restart_apache()


def restart_apache():
    sudo('/etc/init.d/apache2 restart')
