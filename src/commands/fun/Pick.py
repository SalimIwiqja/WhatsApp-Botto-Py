import random
from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number  # import the utility

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "pick",
                "aliases": [],
                "category": "fun",
                "description": {
                    "content": "Picks a random user from the group.",
                    "usage": "<optional_text>",
                },
                "group": True,
                "exp": 4,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            members = M.group.Participants
            if not members:
                return self.client.reply_message(
                    "⚠️ No *members* found in this group.", M
                )

            # Normalize all member numbers
            participants_numbers = [
                clean_number(p.JID.User) for p in members
            ]
            picked_number = random.choice(participants_numbers)
            tag_text = contex.text.strip() if contex.text else "Random_Pick"

            self.client.reply_message(
                f"🎲 *{tag_text}:* @{picked_number}", M
            )

        except Exception as e:
            self.client.reply_message("⚠️ Failed to pick a user.", M)
            self.client.log.error(f"[PickCommandError] {e}")
