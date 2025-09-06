import random
from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number  # import the utility

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ship",
                "aliases": ["shipper"],
                "category": "fun",
                "description": {
                    "content": "Ship two users and get their love percentage ♥",
                    "usage": "<@mention> | <quote>",
                },
                "group": True,
                "exp": 5,
            },
        )

    def exec(self, M: MessageClass, _):
        users = M.mentioned or []
        if M.quoted_user and M.quoted_user not in users:
            users.append(M.quoted_user)

        while len(users) < 2:
            if M.sender not in users:
                users.append(M.sender)
            else:
                break

        if len(users) < 2:
            return self.client.reply_message(
                "❌ Please mention or reply to *someone* to ship with.", M
            )

        if users[0] == M.sender:
            users = users[::-1]

        percentage = self.client.utils.get_random_int(0, 100)

        if percentage < 10:
            level = "Awful 💀"
        elif percentage < 25:
            level = "Very Bad 💢"
        elif percentage < 40:
            level = "Poor 💧"
        elif percentage < 55:
            level = "Average 😐"
        elif percentage < 75:
            level = "Good 🙂"
        elif percentage < 90:
            level = "Great 💖"
        else:
            level = "Amazing 💞"

        first = clean_number(users[0].number)
        second = clean_number(users[1].number)

        message = (
            "```🔺 Compatibility Meter 🔺```\n\n"
            f"💖 @{first} x @{second} 💖\n"
            f"*🔻 {percentage}% {level} 🔻*"
        )

        self.client.reply_message(message, M)
