<VirtualHost *:80>
    ServerName %(server_name)s
    WSGIDaemonProcess %(project_name)s processes=5 python-path=/var/www/%(project_name)s/src:/var/www/%(project_name)s/env/lib/python2.7/site-packages threads=1
    WSGIProcessGroup %(project_name)s
    WSGIScriptAlias / /var/www/%(project_name)s/src/childsos/wsgi.py

    Alias /static /var/www/%(project_name)s/src/static
    Alias /media  /var/www/%(project_name)s/src/media

    <Directory /var/www/%(project_name)s/src//media/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
