from errbot import BotPlugin, botcmd, re_botcmd


class Notes(BotPlugin):
    """
    Remember and respond notes by keywords.
    """

    def __init__(self, *args, **kwargs):
        self.creating = None
        super().__init__(*args, **kwargs)

    # callback_message 函式不知道為何沒動作
    # 所以只好使用 regular 捕捉所有訊息
    @re_botcmd(pattern=r".*", prefixed=False)
    def messages_filter(self, message, match):
        """捕獲訊息並判斷是否記錄到對應的 Note"""
        content = message.body.strip()
        username = message.frm
        channel = message.frm.room if message.is_group else message.frm
        channel_str = '{}'.format(channel)

        if not content:
            return

        if content == '!end':
            yield "完成記錄 {} 。".format(self.creating)
            self.creating = None

        if self.creating:
            key = self.creating
            _d = {}
            _d = self[key]
            if _d['author'] == username and _d['channel'] == channel_str:
                _d['content'].append(content)
                self[key] = _d
            else:
                return # 發言人與作者不同，發言不在同一頻道，則不添加內容到筆記
        else:
            return # creating 為空表示目前沒有任何筆記在創建狀態，缺點是同一時間只能有一筆在創建

    @botcmd
    def note_set(self, message, args):
        """建立 Note"""
        key = args
        username = message.frm
        channel = message.frm.room if message.is_group else message.frm
        self.creating = key
        _d = {}
        self[key] = _d
        with self.mutable(key) as _d:
            _d['author'] = username
            _d['channel'] = '{}'.format(channel)
            _d['content'] = []
        yield "開始記錄 {} ：".format(key)

    @botcmd(template="raw")
    def note_get(self, message, args):
        """讀取 Note"""
        key = args
        content = "\n".join(self[key]['content'])
        return { 'key': key, 'content': content }

    @botcmd
    def note_rm(self, message, args):
        """刪除 Note"""
        key = args
        if key in self:
            content = "\n".join(self[key]['content'])
            del self[key]
            yield "刪除：{}".format(key)
            yield "{}".format(content)
        else:
            yield "{} 不存在。".format(key)

    @botcmd(template="markdown")
    def note_list(self, message, args):
        """條列 Note"""
        content = "\n".join(list(self.keys()))
        return { 'content': content }
