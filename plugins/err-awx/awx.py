from errbot import BotPlugin, botcmd

import os
import json
import subprocess

class Awx(BotPlugin):
    """
    Ansible Tower Command Line Helper
    """

    def __init__(self, *args, **kwargs):
        self.project = None
        self.env = os.environ.copy()
        super().__init__(*args, **kwargs)

    def _run_command(self, cmd_list):
        process = subprocess.Popen(
                    cmd_list,
                    env=self.env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
        stdout, stderr = process.communicate()
        return { 'stdout': stdout, 'stderr': stderr }

    @botcmd(template="json")
    def awx_ping(self, message, args):
        """Get AWX base infomation."""
        cmd = ['awx', 'ping']
        result = self._run_command(cmd)
        return result

    @botcmd(template="json")
    def awx_job_templates_launch(self, message, args):
        """Launch AWX job by specified job template id."""
        cmd = ['awx', 'job_templates', 'launch', args]
        result = self._run_command(cmd)
        return result

    @botcmd(template="json")
    def awx_job_templates_list(self, message, args):
        """List AWX job templates."""
        cmd =['awx', 'job_templates', 'list']
        result = self._run_command(cmd)
        return result

    @botcmd(template="markdown")
    def awx_projects_list(self, message, args):
        """List AWX projects."""
        cmd =['awx', 'projects', 'list']
        result = self._run_command(cmd)
        projects = json.loads(result['stdout'])
        content = []
        for project in projects['results']:
            content.append("專案編號：{}".format(project['id']))
            content.append("專案名稱：{}".format(project['name']))
            content.append("專案源碼：{}".format(project['scm_url']))
            content.append("專案版本：{}".format(project['scm_revision']))
            content.append("---")
        return { 'content': content }
