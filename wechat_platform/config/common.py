# -*- coding: utf-8 -*-
"""
Django settings for wechat_platform project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join, dirname

from configurations import Configuration, values

BASE_DIR = dirname(dirname(__file__))


class Common(Configuration):
    PROJECT_DIR = BASE_DIR

    # APP CONFIGURATION
    DJANGO_APPS = (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Useful template tags:
        # 'django.contrib.humanize',

        # Admin
        # 'django.contrib.admin',
    )
    THIRD_PARTY_APPS = (
        'crispy_forms',  # Form layouts
        'rest_framework',
        'wechat_sdk.context.framework.django',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'system.users',
        'system.official_account',
        'system.request',
        'system.rule',
        'system.rule_match',
        'system.keyword',
        'system.setting',
        'system.plugin',
        'system.library.text',

        'admin.dashboard',
        'admin.user',
        'admin.official_account',
    )

    # Wechat Plugin App
    PLUGIN_APPS = (

    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + PLUGIN_APPS
    # END APP CONFIGURATION

    # MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    # END MIDDLEWARE CONFIGURATION

    # MIGRATIONS CONFIGURATION
    MIGRATION_MODULES = {
        'sites': 'contrib.sites.migrations'
    }
    # END MIGRATIONS CONFIGURATION


    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = "CHANGEME!!!"
    # END SECRET CONFIGURATION

    # FIXTURE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )
    # END FIXTURE CONFIGURATION

    # EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    # END EMAIL CONFIGURATION

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ('doraemonext', 'doraemonext@gmail.com'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    # END MANAGER CONFIGURATION

    # CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify (used on heroku) is painful to install on windows.
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': ''
        }
    }
    # END CACHING

    # GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'Asia/Shanghai'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'zh-cn'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    # END GENERAL CONFIGURATION

    # TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    # See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    # END TEMPLATE CONFIGURATION

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    # END MEDIA CONFIGURATION

    # URL Configuration
    ROOT_URLCONF = 'urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'wsgi.application'
    # End URL Configuration

    # AUTHENTICATION CONFIGURATION
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
    )

    # SLUGLIFIER
    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    # END SLUGLIFIER

    # LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s] %(levelname)s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'development_logfile': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.FileHandler',
                'filename': os.path.join(PROJECT_DIR, 'logs/development.log'),
                'formatter': 'verbose'
            },
            'production_logfile': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'logging.FileHandler',
                'filename': os.path.join(PROJECT_DIR, 'logs/production.log'),
                'formatter': 'simple'
            },
        },
        'loggers': {
            # 系统核心日志
            'system.core': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.keyword': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.library': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.listen': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.official_account': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.plugin': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.request': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.rule': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.rule_match': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.setting': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },
            'system.users': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },

            # 插件日志
            'plugins': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },

            # API日志
            'api': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
                'level': 'DEBUG',
            },

            'django': {
                'handlers': ['console', 'development_logfile', 'production_logfile'],
            },
            'py.warnings': {
                'handlers': ['console', 'development_logfile'],
            },
        }
    }
    # END LOGGING CONFIGURATION

    AUTH_USER_MODEL = 'users.User'

    # Your common stuff: Below this line define 3rd party libary settings
    USERNAME_MIN_LEN = 2
    USERNAME_MAX_LEN = 30
    PASSWORD_MIN_LEN = 4
    PASSWORD_MAX_LEN = 60
    NICKNAME_MIN_LEN = 1
    NICKNAME_MAX_LEN = 30
    GROUP_NAME_MAX_LEN = 80
    OFFICIAL_ACCOUNT_NAME_MAX_LEN = 100
    OFFICIAL_ACCOUNT_ORIGINAL_MAX_LEN = 30
    OFFICIAL_ACCOUNT_WECHAT_MAX_LEN = 100