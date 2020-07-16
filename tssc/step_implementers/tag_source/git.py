"""
Step Implementer for the tag-source step for Git.
"""

from tssc import TSSCFactory
from tssc import StepImplementer
from tssc import DefaultSteps
import sh
import os

DEFAULT_ARGS = {}

class Git(StepImplementer):
    """
    StepImplementer for the tag-source step for Git.
    """

    def __init__(self, config, results_file):
        super().__init__(config, results_file, DEFAULT_ARGS)

    @classmethod
    def step_name(cls):
        return DefaultSteps.TAG_SOURCE

    def _validate_step_config(self, step_config):
        """
        Function for implementers to override to do custom step config validation.

        Parameters
        ----------
        step_config : dict
            Step configuration to validate.
        """

    def _run_step(self, runtime_step_config):
        username_env_var = runtime_step_config['username-env-var']
        password_env_var = runtime_step_config['password-env-var']
        repo_root = runtime_step_config['repo-root']

        if not os.environ.get(username_env_var):
            raise ValueError('The value provided in the step config for username-env-var, ' + username_env_var + ', is not set as a environment variable')
        elif not os.environ.get(password_env_var):
            raise ValueError('The value provided in the step config for password-env-var, ' + password_env_var + ', is not set as a environment variable')

        # Getting the semantic version information from the hopefully previously run generate-metadata step
        print(self.current_results())
        generate_metadata_step_results = self.get_step_results('generate-metadata')
        if 'version' in generate_metadata_step_results:
            version = runtime_step_config['version']
        else:
            raise ValueError('The version information was not found from the generate-metadata step')

        git = sh.git.bake(_cwd=repo_root)
        git.tag(version)
        #process1_args = 'git tag'
        #process2_args = 'git config --get remote.origin.url'
        #process3_args = "git push http://${ + " username_env_var + " }:${" + password_env_var + "}@gitea.apps.tssc.rht-set.com/tssc-references/tssc-reference-app-quarkus-rest-json.git --tags"

        results = {
        }

        return results

# register step implementer
TSSCFactory.register_step_implementer(Git, True)
