import os
from pathlib import Path
import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures
import cloudinary
import cloudinary.uploader
import cloudinary.api



# --- DATABASE & MARIADB FIXES ---
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# Bypass Version Check & Fix MariaDB 10.4 "RETURNING" Error
BaseDatabaseWrapper.check_database_version_supported = lambda *args, **kwargs: None
DatabaseFeatures.can_return_columns_from_insert = property(lambda *args: False)
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda *args: False)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-smx)75o-+^et-#g%x3_qu#jwe!q8zxt6#0w3)8nqcth#2l^bmx'
DEBUG = True
ALLOWED_HOSTS = ['*']

# --- APPS ---
INSTALLED_APPS = [
    'cloudinary_storage',  # MUST stay above staticfiles
    'accounts',
    'resources',
    'cloudinary',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sanaa_sync_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# --- CLOUDINARY & MEDIA ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'djmjge5xu',
    'API_KEY': '615249957438784',
    'API_SECRET': 'f439Fo3kxtBvEfcfDZQyao3PKM0'
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# --- AUTH & STATIC ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
 
STATIC_URL = 'static/'
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile_view'
LOGOUT_REDIRECT_URL = 'landing_page'




# Explicitly configure the Cloudinary SDK
cloudinary.config(
    cloud_name = CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key = CLOUDINARY_STORAGE['API_KEY'],
    api_secret = CLOUDINARY_STORAGE['API_SECRET'],
    secure = True
)

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tofina41@gmail.com'
EMAIL_HOST_PASSWORD = 'vbakfcyysfqjymou'