from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number
from utils import get_rank, ranks  # assuming `ranks` is a dict with exp thresholds


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "rank",
                "category": "core",
                "description": {
                    "content": "Show your current rank and next promotion info."
                },
                "aliases": ["lvl", "level"],
                "exp": 3,
            },
        )

    def exec(self, M: MessageClass, _):
        sender_number = clean_number(M.sender.number)
        user = self.client.db.get_user_by_number(sender_number)
        exp = user.exp
        current_rank = get_rank(exp)
        current_name = current_rank["name"]
        current_data = current_rank["data"]

        next_rank = None
        for _, rank_info in ranks.items():
            if rank_info["exp"] > exp:
                next_rank = get_rank(rank_info["exp"])
                break

        if not next_rank:
            next_rank = current_rank
            next_text = "🎉 You have reached the highest rank!"
        else:
            remaining = next_rank["data"]["exp"] - exp
            next_text = f"🍥 *Next Rank:* {next_rank['name']} {next_rank['data']['emoji']} ({remaining} exp required)"

        reply = f"""
🏷️  *Username:* {M.sender.username}

🪄 *Experience:* {exp}

🏆 *Rank:* {current_name} {current_data['emoji']}

{next_text}
"""
        self.client.reply_message(reply.strip(), M)
