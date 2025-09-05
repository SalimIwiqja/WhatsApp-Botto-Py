from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv


class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        sender_jid = self.Info.MessageSource.Sender.User
        # Safely get sender username
        try:
            contact = client.contact.get_contact(sender_jid)
            username = getattr(contact, "PushName", sender_jid)
        except Exception:
            username = sender_jid

        self.sender = DynamicConfig(
            {
                "number": sender_jid,
                "username": username,
            }
        )

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
                    quoted_number = ctx_info.participant.split("@")[0]
                    try:
                        quoted_contact = client.contact.get_contact(quoted_number)
                        quoted_username = getattr(quoted_contact, "PushName", quoted_number)
                    except Exception:
                        quoted_username = quoted_number

                    self.quoted_user = DynamicConfig(
                        {
                            "number": quoted_number,
                            "username": quoted_username,
                        }
                    )

            # Handle mentioned users safely
            for jid in ctx_info.mentionedJID:
                number = jid.split("@")[0]
                try:
                    contact = client.contact.get_contact(number)
                    username = getattr(contact, "PushName", number)
                except Exception:
                    username = number

                self.mentioned.append(
                    DynamicConfig(
                        {
                            "number": number,
                            "username": username,
                        }
                    )
                )

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = self.__client.utils.extract_numbers(self.content)

        if self.chat == "group":
            try:
                self.group = self.__client.get_group_info(self.gcjid)
            except Exception:
                self.group = None

            self.isAdminMessage = (
                self.sender.number
                in self.__client.filter_admin_users(self.group.Participants)
                if self.group
                else False
            )

        return self

    def raw(self):
        return self.__M
