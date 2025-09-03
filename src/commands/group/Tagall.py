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
                    "content": "Tag everyone in the group, one per line.",
                    "usage": "",
                },
                "exp": 0,
                "group": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        # Fetch group info
        try:
            group_info = self.client.get_group(M.gcjid)  # Updated method
        except Exception as e:
            return self.client.reply_message(f"⚠️ Failed to get group info: {e}", M)

        # Try both possible participant lists
        participants = getattr(group_info, "participants", None)
        if not participants:
            participants = getattr(group_info, "members", [])

        if not participants:
            return self.client.reply_message("⚠️ No members found in this group.", M)

        # Check if sender is admin
        admins = [p.id for p in participants if getattr(p, "admin", False)]
        if M.sender.number not in [a.split("@")[0] for a in admins]:
            return self.client.reply_message("⚠️ Only *group admins* can use this command.", M)

        # Build mentions
        mentions = [p.id for p in participants if p.id != self.client.config.number]
        if not mentions:
            return self.client.reply_message("⚠️ No other members to tag.", M)

        # Build message text with one user per line
        text_lines = [f"@{m.split('@')[0]}" for m in mentions]
        text = "📢 *Tagging everyone in the group:*\n\n" + "\n".join(text_lines)

        # Send message with mentions
        self.client.send_message(M.gcjid, text, mentions=mentions)
