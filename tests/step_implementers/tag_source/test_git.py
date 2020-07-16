import pytest
from testfixtures import TempDirectory
import yaml
import os

from tssc import TSSCFactory
from tssc.step_implementers.tag_source import Git

from test_utils import *

def test_tag_source_default():
    with TempDirectory() as temp_dir:
        config = {
            'tssc-config': {}
        }
        expected_step_results = {'tssc-results': {'tag-source': {}}}

        run_step_test_with_result_validation(temp_dir, 'tag-source', config, expected_step_results)

def test_tag_source_specify_git_implementer():
    with TempDirectory() as temp_dir:
        config = {
            'tssc-config': {
                'tag-source': {
                    'implementer': 'Git',
                    'config': {
                        'username-env-var': 'GIT_USERNAME',
                        'password-env-var': 'GIT_PASSWORD'
                    }
                }
            }
        }
        expected_step_results = {
            'tssc-results': {
                'generate-metadata': {
                    'app-version': 'app_version',
                    'pre-release': 'feature_test0',
                    'build': 'build',
                    'version': 'version',
                    'image-tag': 'image_tag'
                }
            },
            'tag-source': {}
        }
        #expected_step_results = {'tssc-results': {'tag-source': {}}}

        # Using this try/finally block so that we can temporarily set environment variables for unit testing
        _environ = dict(os.environ)  # or os.environ.copy()
        try:
            os.environ["GIT_USERNAME"] = "test_username"
            os.environ["GIT_PASSWORD"] = "test_password"
            run_step_test_with_result_validation(temp_dir, 'tag-source', config, expected_step_results, runtime_args={'repo-root': str(temp_dir.path)})
        finally:
            os.environ.clear()
            os.environ.update(_environ)
