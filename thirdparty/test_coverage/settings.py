"""
Copyright 2009 55 Minutes (http://www.55minutes.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Specify the coverage test runner
COVERAGE_TEST_RUNNER = 'test_coverage.coverage_runner.run_tests'

# Specify regular expressions of code blocks the coverage analyzer should
# ignore as statements (e.g. ``raise NotImplemented``).
# These statements are not figured in as part of the coverage statistics.
# This setting is optional.
COVERAGE_CODE_EXCLUDES = [
    'def __unicode__\(self\):', 'def get_absolute_url\(self\):',
    'from .* import .*', 'import .*', '#.*'
    ]
    
# Specify a list of regular expressions of paths to exclude from
# coverage analysis.
# Note these paths are ignored by the module introspection tool and take
# precedence over any package/module settings such as:
# TODO: THE SETTING FOR MODULES
# Use this to exclude subdirectories like ``r'.svn'``, for example.
# This setting is optional.
COVERAGE_PATH_EXCLUDES = [r'.svn']

# Specify a list of additional module paths to include
# in the coverage analysis. By default, only modules within installed
# apps are reported. If you have utility modules outside of the app
# structure, you can include them here.
# Note this list is *NOT* regular expression, so you have to be explicit,
# such as 'myproject.utils', and not 'utils$'.
# This setting is optional.
COVERAGE_ADDITIONAL_MODULES = []

# Specify a list of regular expressions of module paths to exclude
# from the coverage analysis. Examples are ``'tests$'`` and ``'urls$'``.
# This setting is optional.
COVERAGE_MODULE_EXCLUDES = ['tests$', 'settings$','urls$', 'common.views.test',
                            '__init__', 'django']

# Specify the directory where you would like the coverage report to create
# the HTML files.
# You'll need to make sure this directory exists and is writable by the
# user account running the test.
# You should probably set this one explicitly in your own settings file.
COVERAGE_REPORT_HTML_OUTPUT_DIR = '/my_home/test_html'

