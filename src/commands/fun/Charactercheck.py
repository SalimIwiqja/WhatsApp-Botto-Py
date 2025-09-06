import random
from libs import BaseCommand, MessageClass

CHECK_OPTIONS = [
    "awesomecheck",
    "greatcheck",
    "gaycheck",
    "cutecheck",
    "lesbiancheck",
    "hornycheck",
    "prettycheck",
    "lovelycheck",
    "uglycheck",
    "beautifulcheck",
    "handsomecheck",
    "charactercheck",
]

CHARACTER_TRAITS = [
    "Compassionate",
    "Generous",
    "Grumpy",
    "Forgiving",
    "Obedient",
    "Good",
    "Simp",
    "Kind-Hearted",
    "Patient",
    "UwU",
    "Top (anyway)",
    "Helpful",
]


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "charactercheck",
                "aliases": CHECK_OPTIONS,
                "category": "fun",
                "description": {
                    "content": "Checks how much someone is something (e.g., awesome, gay, pretty).",
                    "usage": "<check_type> <@mention> | <quote>",
                },
                "exp": 10,
            },
        )

    def exec(self, M: MessageClass, contex):
        cmd = contex.cmd.lower()
        raw_arg = contex.text.strip().lower() if contex.text else ""

        is_raw = cmd in CHECK_OPTIONS
        check = cmd if is_raw else raw_arg.split(" ")[0]

        if not check or check not in CHECK_OPTIONS:
            check_list = "\n- " + "\n- ".join([c for c in CHECK_OPTIONS])
            usage_msg = f"""🎃 *Available Checks:*{check_list}

🛠️ *Usage:* {self.client.config.prefix}checkuser (check) [@tag or quote user]
Example: {self.client.config.prefix}awesomecheck"""
            return self.client.reply_message(usage_msg, M)

        # Determine target
        target = M.quoted_user or (M.mentioned[0] if M.mentioned else M.sender)
        target_number = target.number
        target_tag = f"@{target_number}"

        # Result generation
        percentage = random.randint(1, 100)
        if check == "charactercheck":
            trait = random.choice(CHARACTER_TRAITS)
            result = f"{percentage}% {trait}"
        else:
            title = check.replace("check", "")
            result = f"{percentage}% {title}"

        reply = f"""🎯 *{check.upper()} Result*

{target_tag} is `{result}`"""

        self.client.reply_message(reply, M)
