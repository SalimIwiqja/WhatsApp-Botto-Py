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

        # Check if sender is admin
        admins = [p.id for p in participants if p.admin]
        if M.sender.number not in [a.split("@")[0] for a in admins]:
            return self.client.reply_message("⚠️ Only *group admins* can use this command.", M)

        # Build mentions
        mentions = [p.id for p in participants if p.id != self.client.config.number]
        if not mentions:
            return self.client.reply_message("⚠️ No members to tag.", M)

        text = "📢 *Tagging everyone in the group:*\n\n"
        text += "\n".join([f"@{m.split('@')[0]}" for m in mentions])

        self.client.send_message(
            M.gcjid,
            text,
            mentions=mentions,
        )
