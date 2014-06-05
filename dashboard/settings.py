"""
Django settings for dashboard project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$ay*0mfo))zn+@xu+10wf)asc50353^%)crbup%^gy72$lsm(t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dashboard.urls'

WSGI_APPLICATION = 'dashboard.wsgi.application'


#AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
OPENSTACK_KEYSTONE_URL = "http://192.168.2.10:5000/v2.0"

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    #"/home/cloudopen/luxy/demodashboard/dashboard/templates",
)

# template loader
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader'
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (
    #"/home/cloudopen/luxy/demodashboard/dashboard/static",
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'
#STATIC_ROOT = "/home/cloudopen/luxy/demodashboard/dashboard/static"

AUTH_URL = "http://192.168.2.10:5000/v3"
AUTH_URL_V2 = "http://192.168.2.10:5000/v2.0"
