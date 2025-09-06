from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tagall",
                "category": "group",
                "aliases": ["all"],
                "description": {
                    "content": "Mention all members in the group.",
                    "usage": "",
                },
                "exp": 5,
                "group": True,
                "devOnly": False,
            },
        )

    def exec(self, M: MessageClass, contex):
        if M.chat != "group":
            return self.client.reply_message(
                "⚠️ This command can only be used in a group.", M
            )

        group = M.group
        if not group or not hasattr(group, "Participants"):
            return self.client.reply_message(
                "⚠️ Failed to get group info. No participants found.", M
            )

        mention_jids = []
        text = "📢 Attention everyone!\n\n"

        for participant in group.Participants:
            number = getattr(participant.JID, "User", None)
            if not number:
                continue
            mention_jids.append(participant.JID)
            text += f"@{number} "

        # Use 'mention' keyword instead of 'context'
        self.client.send_message(M.gcjid, text.strip(), mention=mention_jids)
