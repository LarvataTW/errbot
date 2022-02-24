from errbot import BotPlugin, botcmd

import subprocess

class Awx(BotPlugin):
    """
    Ansible Tower Command Line Helper
    """

    def __init__(self, *args, **kwargs):
        self.project = None
        super().__init__(*args, **kwargs)

    @botcmd
    def awx_info(self, message, args):
        """Get AWX info"""
        process = subprocess.Popen(['awx', 'projects', 'list'],
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        yield stdout
        yield stderr
