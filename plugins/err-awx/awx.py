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

    @botcmd
    def awx_info(self, message, args):
        """Get AWX info"""
        process = subprocess.Popen(
                    ['awx', 'ping'],
                    env=self.env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
        stdout, stderr = process.communicate()
        yield stdout
        yield stderr
