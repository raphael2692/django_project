import os
from pathlib import Path

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# A secret key for a particular Django installation. This is used to provide cryptographic signing.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-l$p&ko&(z3=d-9rbi#$sglr&7)jw72zgb1xq)u2q1&^qm&dih7')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode should be False in a production environment.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "django"]

# The entry point for the WSGI-compatible web servers to serve your project.
WSGI_APPLICATION = 'project.wsgi.application'

# The entry point for ASGI-compatible web servers to serve your project.
ASGI_APPLICATION = 'project.asgi.application'

# The Python path to your project's root URLconf.
ROOT_URLCONF = 'project.urls'

# The default primary key field type to use for models that don't have a field with primary_key=True.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

# Application definition
INSTALLED_APPS = [
    # Django Channels
    'daphne',
    'channels',

    # Django Contrib Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'allauth',
    'allauth.account',
    'django_htmx',

    # Your Apps
    'core',
    'notifications',
    'todo'
]


# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Third-Party Middleware
    'allauth.account.middleware.AccountMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]


# ==============================================================================
# TEMPLATES
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / 'templates'], # Global templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==============================================================================
# DATABASES
# ==============================================================================
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# AUTHENTICATION & PASSWORD VALIDATION
# ==============================================================================
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Authentication backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


# ==============================================================================
# INTERNATIONALIZATION (I18N)
# ==============================================================================
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Default language code for this installation.
LANGUAGE_CODE = 'it'

# The time zone for this installation.
TIME_ZONE = 'Europe/Rome'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# A list of all available languages for this site.
LANGUAGES = [
    ('it', 'Italiano'),
    ('en', 'English'),
]

# The directories where Django looks for translation files.
LOCALE_PATHS = [BASE_DIR / 'locale']


# ==============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# ==============================================================================
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = 'static/'


# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

# The backend to use for sending emails.
# For development, 'console.EmailBackend' logs emails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ==============================================================================
# THIRD-PARTY LIBRARIES CONFIGURATION
# ==============================================================================

# ------------------------------------------------------------------------------
# REDIS
# ------------------------------------------------------------------------------
# Host for Redis, used by Celery and Channels.
# Defaults to localhost if not set in environment variables.
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")

# ------------------------------------------------------------------------------
# CELERY
# ------------------------------------------------------------------------------
# Configuration for Celery, the asynchronous task queue.
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# ------------------------------------------------------------------------------
# CHANNELS
# ------------------------------------------------------------------------------
# Configuration for Channels, which handles WebSockets and other long-running connections.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}
