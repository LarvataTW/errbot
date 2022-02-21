from errbot import BotPlugin, botcmd, re_botcmd


class Notes(BotPlugin):
    """
    Remember and respond notes by keywords.
    """

    def __init__(self, *args, **kwargs):
        self.creating = None
        self.notes = dict()
        super().__init__(*args, **kwargs)

    # callback_message 函式不知道為何沒動作
    # 所以只好使用 regular 捕捉所有訊息
    @re_botcmd(pattern=r".*", prefixed=False)
    def messages_filter(self, message, match):
        content = message.body.strip()
        username = message.frm
        channel = message.frm.room if message.is_group else message.frm
        channel_str = '{}'.format(channel)

        if not content:
            return

        if content == '#end':
            yield "完成記錄 {} 。".format(self.creating)
            self.creating = None

        if self.creating:
            key = self.creating
            if self.notes[key]['author'] == username and self.notes[key]['channel'] == channel_str:
                self.notes[key]['content'].append(content)
            else:
                return # 發言人與作者不同，發言不在同一頻道，則不添加內容到筆記
        else:
            return # creating 為空表示目前沒有任何筆記在創建狀態，缺點是同一時間只能有一筆在創建

    @botcmd
    def note_set(self, message, args):
        """Create a note"""
        key = args
        username = message.frm
        channel = message.frm.room if message.is_group else message.frm
        self.creating = key
        self.notes[key] = {}
        self.notes[key]['author'] = username
        self.notes[key]['channel'] = '{}'.format(channel)
        self.notes[key]['content'] = []
        yield "開始記錄 {} ：".format(key)

    @botcmd(template="content")
    def note_get(self, message, args):
        """Read a note"""
        key = args
        content = "\n".join(self.notes[key]['content'])
        return { 'key': key, 'content': content }
