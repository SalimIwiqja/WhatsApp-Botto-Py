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
        # Fetch group participants using the correct client API
        try:
            group_info = self.client.get_group_info(M.gcjid)
            participants = group_info.participants
        except Exception as e:
            return self.client.reply_message(
                f"⚠️ Failed to get group info: {e}", M
            )

        # Check if sender is admin
        sender_id = M.sender.number + "@s.whatsapp.net"
        admins = [p.id for p in participants if getattr(p, "admin", False)]
        if sender_id not in admins:
            return self.client.reply_message(
                "⚠️ Only *group admins* can use this command.", M
            )

        # Prepare mentions and text
        mentions = [p.id for p in participants if p.id != self.client.config.number]
        if not mentions:
            return self.client.reply_message("⚠️ No members to tag.", M)

        text_lines = [f"@{m.split('@')[0]}" for m in mentions]
        text = "📢 *Tagging everyone in the group:*\n\n" + "\n".join(text_lines)

        # Send message with mentions
        self.client.send_message(
            M.gcjid,
            text,
            mentions=mentions
        )
