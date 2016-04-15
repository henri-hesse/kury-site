# Kiipeilyurheilijat ry website

## Setting up development installation

Follow the standard installation of Python, Django & MariaDB.
https://docs.djangoproject.com/en/1.9/intro/install/

Set up the database settings in kury/settings.py file. You need to create
database user for the website to use and empty database with all permissions
enabled for that user in the database.

Once you have everything set up, cd to project root & migrate your database

  python manage.py migrate

Install these extra packages:

* pip install markdown
* pip install pytz
* pip install django-imagekit

## Production, NOT COMPLETE!

Install python-imaging and python-mysql packages
Make media directory writeable by django
