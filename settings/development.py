from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

# Logging settings
INTERNAL_IPS = ('127.0.0.1', )
LOGGING_LOG_SQL = True
LOGGING_INTERCEPT_REDIRECTS = True

# DB Stuff
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'deploy/dev.db'

# URL Stuff
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# Test type stuff
INSTALLED_APPS += ("events.tests", "utils.tests",)
TEST_RUNNER = 'test_coverage.coverage_runner.run_tests'
COVERAGE_REPORT_HTML_OUTPUT_DIR = './deploy/reports'
COVERAGE_CODE_EXCLUDES = ['def __unicode__\(self\):', 'def get_absolute_url\(self\):', 'from .* import .*', 'import .*', '^#.*']

