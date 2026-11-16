import sys
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

env = environ.Env(DEBUG=(bool, False))
environment_file = BASE_DIR / '.env'
if environment_file.exists():
    environ.Env.read_env(environment_file)

DEBUG = env.bool('DEBUG', default=False)
TESTING = 'test' in sys.argv

SECRET_KEY = env('DJANGO_SECRET_KEY', default='').strip()
if not SECRET_KEY:
    if DEBUG or TESTING:
        SECRET_KEY = 'development-only-not-for-production-change-before-deploying'
    else:
        raise ImproperlyConfigured('DJANGO_SECRET_KEY es obligatorio cuando DEBUG=False.')


def csv_env(name, default=''):
    return [item.strip() for item in env(name, default=default).split(',') if item.strip()]


ALLOWED_HOSTS = csv_env('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
CSRF_TRUSTED_ORIGINS = csv_env('DJANGO_CSRF_TRUSTED_ORIGINS')
if '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('DJANGO_ALLOWED_HOSTS no admite comodines.')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.accounts.apps.AccountsConfig',
    'apps.catalog.apps.CatalogConfig',
    'apps.events.apps.EventsConfig',
    'apps.moderation.apps.ModerationConfig',
    'apps.api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'radar_api.cache_control.PublicContentCacheControlMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'radar_api.urls'
WSGI_APPLICATION = 'radar_api.wsgi.application'
ASGI_APPLICATION = 'radar_api.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

database_url = env('DATABASE_URL', default='').strip()
if not database_url:
    if DEBUG or TESTING:
        database_url = f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    else:
        raise ImproperlyConfigured('DATABASE_URL es obligatorio cuando DEBUG=False.')

DATABASES = {'default': environ.Env.db_url_config(database_url)}
DATABASES['default']['CONN_MAX_AGE'] = 60
if not DEBUG and not TESTING and DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql':
    raise ImproperlyConfigured('Producción requiere PostgreSQL en DATABASE_URL.')

AUTH_USER_MODEL = 'accounts.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/backend-static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.api.pagination.RadarPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': env('API_ANON_RATE', default='120/hour'),
        'user': env('API_USER_RATE', default='1200/hour'),
    },
    'EXCEPTION_HANDLER': 'apps.api.exceptions.api_exception_handler',
    'NUM_PROXIES': env.int('API_NUM_PROXIES', default=1),
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', default=3600)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False
    )
    SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=False)
    SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('DJANGO_LOG_LEVEL', default='INFO'),
    },
}

# Vite debe consumir /api a través de un proxy local o del mismo origen. No se
# habilita CORS global ni se aceptan orígenes comodín por defecto.
FRONTEND_ORIGIN = env('FRONTEND_ORIGIN', default='http://127.0.0.1:5173').rstrip('/')
