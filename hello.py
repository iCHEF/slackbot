# -*- coding: utf-8 -*-
def hello_msg(msg_text):

    if u"我愛你" in msg_text:
        text = u"人家... 人家才不愛你呢！哼！！"
    else:
        text = u"你... 你一直叫我，我也不會理你的喲 >////<"

    args = {
        # "channel": channel,
        "text": text.encode("utf-8"),
        "username": u"愛雪芙羅伯特".encode("utf-8"),
        "as_user": False,
    }

    return args