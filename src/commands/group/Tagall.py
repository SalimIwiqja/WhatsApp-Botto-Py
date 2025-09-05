from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tagall",
                "category": "group",
                "aliases": ["all", "everyone"],
                "description": {
                    "content": "Tag everyone in the group.",
                    "usage": "",
                },
                "exp": 0,
                "group": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not M.is_group:
            return self.client.reply_message("⚠️ This command only works in groups.", M)

        if not M.is_sender_admin:
            return self.client.reply_message("⚠️ Only *group admins* can use this command.", M)

        try:
            participants = [p for p in M.group_participants if p.number != self.client.config.number]
        except Exception:
            return self.client.reply_message("⚠️ Failed to get group participants.", M)

        if not participants:
            return self.client.reply_message("⚠️ No participants found in the group.", M)

        text = "📢 *Tagging everyone in the group:*\n\n"
        text += "\n".join([f"@{p.number.split('@')[0]}" for p in participants])

        self.client.send_message(
            M.gcjid,
            text,
            mentions=[p.number for p in participants]
        )
