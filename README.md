Platform-Dev
============

VDI-Stack Management Platform Develop Code

## Getting Started

For local development, first create a virtualenv for the project.

```
virtualenv .venv
source .venv/bin/activate
```

Before install python packages, some packages you should be installed.

```
apt-get install python-dev
apt-get install libxml++2.6-2 libxml++2.6-dev
apt-get install libxslt1.1 libxslt1-dev
apt-get install mysql-server
apt-get install libmysqlclient-dev
apt-get install libffi6 libffi-dev
apt-get install libssl1.0.0 libssl-dev
```

Then you can install python packages for the project:

```
pip install -r requirements.txt
```

Configure databases connection in ```dashboard/settings.py```:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'demodashboard',
        'PORT': '3036',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
    }
}
```

then, run command ```python manage.py syncdb``` to init db.
