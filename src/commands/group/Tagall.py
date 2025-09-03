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
        group_metadata = self.client.get_group_metadata(M.gcjid)
        participants = group_metadata.participants

        bot_number_full = f"{self.client.config.number}@s.whatsapp.net"
        sender_number_full = M.sender.number if "@" in M.sender.number else f"{M.sender.number}@s.whatsapp.net"

        # Check if sender is admin
        admins = [p.id for p in participants if getattr(p, "admin", False)]
        if sender_number_full not in admins:
            return self.client.reply_message("⚠️ Only *group admins* can use this command.", M)

        # Build mentions
        mentions = [p.id for p in participants if p.id != bot_number_full]
        if not mentions:
            return self.client.reply_message("⚠️ No members to tag.", M)

        text = "📢 *Tagging everyone in the group:*\n\n"
        text += "\n".join([f"@{m.split('@')[0]}" for m in mentions])

        self.client.send_message(
            M.gcjid,
            text,
            mentions=mentions,
        )
