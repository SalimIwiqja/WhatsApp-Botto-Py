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
        # Use M.group_metadata instead of self.client.get_group_metadata()
        group_metadata = M.group_metadata
        if not group_metadata:
            return self.client.reply_message("⚠️ Unable to fetch group info.", M)

        participants = group_metadata.participants
        if not participants:
            return self.client.reply_message("⚠️ No members in the group.", M)

        # Check if sender is admin
        sender_id = M.sender.number + "@s.whatsapp.net"
        admins = [p.id for p in participants if getattr(p, "admin", False)]
        if sender_id not in admins:
            return self.client.reply_message("⚠️ Only *group admins* can use this command.", M)

        # Build mentions
        bot_number = self.client.config.number + "@s.whatsapp.net"
        mentions = [p.id for p in participants if p.id != bot_number]

        if not mentions:
            return self.client.reply_message("⚠️ No members to tag.", M)

        # Message with one member per line
        text = "📢 *Tagging everyone in the group:*\n\n"
        text += "\n".join([f"@{m.split('@')[0]}" for m in mentions])

        # Send with mentions
        self.client.send_message(M.gcjid, text, mentions=mentions)
