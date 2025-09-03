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
        # Fetch group info from DB
        group = self.client.db.get_group_by_number(M.gcjid)
        if not group:
            return self.client.reply_message("⚠️ Failed to get group info.", M)

        participants = getattr(group, "participants", [])
        admins = getattr(group, "admins", [])

        if not participants:
            return self.client.reply_message("⚠️ No participants found.", M)

        # Check if sender is admin
        if M.sender.number not in admins and M.sender.number != self.client.config.number:
            return self.client.reply_message("⚠️ Only *group admins* can use this command.", M)

        # Build mentions text
        mentions = []
        text_lines = ["📢 *Tagging everyone in the group:*"]
        for p in participants:
            if p != self.client.config.number:  # skip bot itself
                mentions.append(p)
                text_lines.append(f"@{p.split('@')[0]}")

        text = "\n".join(text_lines)

        # Send the message with mentions
        self.client.send_message(
            M.gcjid,
            text,
            mentions=mentions
        )
