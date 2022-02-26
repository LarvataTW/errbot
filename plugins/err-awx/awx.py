from errbot import BotPlugin, botcmd

import os
import subprocess

class Awx(BotPlugin):
    """
    Ansible Tower Command Line Helper
    """

    def __init__(self, *args, **kwargs):
        self.project = None
        self.env = os.environ.copy()
        super().__init__(*args, **kwargs)

    @botcmd(template="json")
    def awx_ping(self, message, args):
        """Get AWX base infomation."""
        process = subprocess.Popen(
                    ['awx', 'ping'],
                    env=self.env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
        stdout, stderr = process.communicate()
        return { 'stdout': stdout, 'stderr': stderr }

    @botcmd(template="json")
    def awx_job_templates_launch(self, message, args):
        """Launch AWX job by specified job template id."""
        process = subprocess.Popen(
                    ['awx', 'job_templates', 'launch', args],
                    env=self.env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
        stdout, stderr = process.communicate()
        return { 'stdout': stdout, 'stderr': stderr }

    @botcmd(template="json")
    def awx_job_templates_list(self, message, args):
        """Launch AWX job by specified job template id."""
        process = subprocess.Popen(
                    ['awx', 'job_templates', 'list'],
                    env=self.env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
        stdout, stderr = process.communicate()
        return { 'stdout': stdout, 'stderr': stderr }
