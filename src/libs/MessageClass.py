import re
from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv

def clean_number(number):
    """Normalize number to E.164 format string."""
    if isinstance(number, int):
        number = str(number)
    return re.sub(r"[^\d+]", "", number)

class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        raw_sender = self.Info.MessageSource.Sender.User
        self.sender = DynamicConfig({
            "number": clean_number(raw_sender),
            "username": getattr(client.contact.get_contact(clean_number(raw_sender)), "PushName", "Unknown"),
        })

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage

                if ctx_info.HasField("participant"):
                    quoted_number = clean_number(ctx_info.participant.split("@")[0])
                    self.quoted_user = DynamicConfig({
                        "number": quoted_number,
                        "username": getattr(client.contact.get_contact(quoted_number), "PushName", "Unknown")
                    })

            for jid in ctx_info.mentionedJID:
                number = clean_number(jid.split("@")[0])
                self.mentioned.append(DynamicConfig({
                    "number": number,
                    "username": getattr(client.contact.get_contact(number), "PushName", "Unknown")
                }))

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = [clean_number(n) for n in self.__client.utils.extract_numbers(self.content)]

        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = (
                self.sender.number in
                [clean_number(p.JID.User) for p in self.__client.filter_admin_users(self.group.Participants)]
            )

        return self

    def raw(self):
        return self.__M
