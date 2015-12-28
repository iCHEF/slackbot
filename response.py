# -*- coding: utf-8 -*-
class Response(object):
    """Response for function that actually do something like weather function

    """
    def __init__(self, text='', username=u"愛雪芙羅伯特".encode("utf-8"), attachments=None):
        super(Response, self).__init__()
        self.text = text
        self.username = username
        self.attachments = attachments

    def get_args(self, channel):
        '''Get full args that send slack message needed

        channel: set channel that this message would be sent
        '''
        args = {
            "channel": channel,
            "text": self.text,
            "username": self.username,
            "as_user": False,
        }
        if self.attachments is not None:
            args['attachments'] = self.attachments
        return args
        