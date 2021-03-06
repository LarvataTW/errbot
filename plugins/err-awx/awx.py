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
        """驗證 AWX 連線與授權"""
        cmd = ['awx', 'ping']
        result = self._run_command(cmd)
        return result

    @botcmd(template="markdown")
    def awx_projects_list(self, message, args):
        """條列 AWX 專案"""
        # TODO: 根據 args 進行搜尋過濾
        # 當 args 為空則列出全部的 projects 資訊
        # 否則列出單一 projects 
        # Example: !awx projects list suzen
        if args:
            cmd =['awx', 'projects', 'list', '--name', args]
        else:
            cmd =['awx', 'projects', 'list', '--all']
        result = self._run_command(cmd)
        projects = json.loads(result['stdout'])
        content = []
        for project in projects['results']:
            content.append("\n")
            content.append("專案編號：{}".format(project['id']))
            content.append("專案名稱：{}".format(project['name']))
            content.append("專案源碼：{}".format(project['scm_url']))
            content.append("專案版本：{}".format(project['scm_revision']))
        return { 'content': "\n".join(content) }

    @botcmd(template="raw")
    def awx_job_templates_list(self, message, args):
        """條列 AWX 任務樣板"""
        # TODO: 根據 args 進行搜尋過濾
        cmd =['awx', 'job_templates', 'list', '--all']
        result = self._run_command(cmd)
        job_templates = json.loads(result['stdout'])
        content = []
        for job_template in job_templates['results']:
            content.append("\n")
            content.append("任務編號：{}".format(job_template['id']))
            content.append("任務名稱：{}".format(job_template['name']))
            content.append("任務腳本：{}".format(job_template['playbook']))
        return { 'content': "\n".join(content) }

    @botcmd(template="raw")
    def awx_job_templates_launch(self, message, args):
        """發射指定編號的 AWX 任務，並回傳 Job 編號"""
        # TODO: 建立互動詢問，確認是否執行，而不是無腦直接執行
        cmd = ['awx', 'job_templates', 'launch', args]
        result = self._run_command(cmd)
        job = json.loads(result['stdout'])
        content = []
        content.append("Job 編號：{}".format(job['id']))
        content.append("Job 連結：{}".format(job['url']))
        content.append("Job 名稱：{}".format(job['name']))
        content.append("Job 狀態：{}".format(job['status']))
        return { 'content': "\n".join(content) }

    @botcmd(template="raw")
    def awx_job_get(self, message, args):
        """取得指定編號的 AWX Job 狀態"""
        cmd = ['awx', 'job', 'get', args]
        result = self._run_command(cmd)
        job = json.loads(result['stdout'])
        content = []
        content.append("Job 編號：{}".format(job['id']))
        content.append("Job 連結：{}".format(job['url']))
        content.append("Job 名稱：{}".format(job['name']))
        content.append("Job 狀態：{}".format(job['status']))
        return { 'content': "\n".join(content) }
