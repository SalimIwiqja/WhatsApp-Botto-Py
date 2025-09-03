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
        # Fetch group from database safely
        try:
            group = self.client.db.get_group_by_number(str(M.gcjid))
        except Exception as e:
            return self.client.reply_message(f"⚠️ Failed to get group info: {e}", M)

        if not group or not getattr(group, "participants", None):
            return self.client.reply_message("⚠️ No participants found in the group.", M)

        # Check if sender is admin
        admins = [str(p.id) for p in group.participants if getattr(p, "admin", False)]
        if str(M.sender.number) not in admins:
            return self.client.reply_message("⚠️ Only group admins can use this command.", M)

        # Build mentions list (exclude bot itself)
        mentions = [str(p.id) for p in group.participants if str(p.id) != self.client.config.number]
        if not mentions:
            return self.client.reply_message("⚠️ No members to tag.", M)

        # Construct text with mentions
        text = "📢 *Tagging everyone in the group:*\n\n"
        text += "\n".join([f"@{m.split('@')[0]}" for m in mentions])

        # Send message with mentions
        self.client.send_message(
            str(M.gcjid),
            text,
            mentions=mentions,
        )
