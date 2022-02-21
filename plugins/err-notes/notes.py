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

        if not content or content.startswith("!"):
            return

        if content == '#end':
            yield "完成記錄 {} 。".format(self.creating)
            self.creating = None

        if self.creating:
            key = self.creating
            self.notes[key].append(content)

    @botcmd
    def note_create(self, message, args):
        """Create a note"""
        key = args
        self.creating = key
        if key not in self.notes:
            self.notes[key] = []
        yield "開始記錄 {} ：".format(key)

    @botcmd
    def note_read(self, message, args):
        """Read a note"""
        yield self.notes[args]
