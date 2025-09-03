from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tagall",
                "category": "group",
                "aliases": [],
                "description": {
                    "content": "Mention all group members.",
                    "usage": "<optional message>",
                },
                "exp": 0,
                "group": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        # Get group ID and sender number
        group_id = M.gcjid
        sender_number = M.sender.number

        try:
            # Fetch group participants and admins
            participants = self.client.get_group_participants(group_id)
            group_admins = [adm.user for adm in self.client.get_group_admins(group_id)]
        except Exception as e:
            return self.client.reply_message(f"⚠️ Error fetching group info: {e}", M)

        # Check if sender is an admin
        if sender_number not in group_admins:
            return self.client.reply_message(
                "⚠️ Only group admins can use this command.", M
            )

        # Optional text after the command
        optional_text = contex.text.strip() if contex.text else ""

        # Build mentions list
        mentions = []
        mention_texts = []
        for member in participants:
            mentions.append(member.user)
            mention_texts.append(f"@{member.user.split('@')[0]}")

        # Final message
        message_to_send = (
            optional_text + "\n\n" if optional_text else ""
        ) + " ".join(mention_texts)

        # Send message with mentions
        try:
            self.client.send_message(
                group_id,
                message_to_send,
                mentions=mentions
            )
        except Exception as e:
            self.client.reply_message(f"⚠️ Failed to tag everyone: {e}", M)
