
import sys
from thirdparty import path

PROJECT_ROOT = path(__file__).abspath().dirname()

sys.path.append(PROJECT_ROOT / 'thirdparty')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jon Raphaelson', 'jonraphaelson@gmail.com'),
)

INTERNAL_IPS = ('127.0.0.1', )

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'deploy/dev.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/New York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = PROJECT_ROOT / 'media'
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '53s-f5k_g(twgd2xbkyuxe&enr-u@!mvuf*5%lm*wj$kl=a1hm'

LOGGING_LOG_SQL = True
LOGGING_INTERCEPT_REDIRECTS = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'djangologging.middleware.LoggingMiddleware',
)

ROOT_URLCONF = 'twid.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT / 'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'utils',
    'events',
)

def on_test(self):
    self.INSTALLED_APPS += ("events.tests", "utils.tests",)
    self.TEST_RUNNER = 'test_coverage.coverage_runner.run_tests'
    self.COVERAGE_REPORT_HTML_OUTPUT_DIR = './deploy/reports'
    self.COVERAGE_CODE_EXCLUDES = [ 'def __unicode__\(self\):', 'def get_absolute_url\(self\):', 'from .* import .*', 'import .*', '^#.*' ]

ON_TEST = on_test
