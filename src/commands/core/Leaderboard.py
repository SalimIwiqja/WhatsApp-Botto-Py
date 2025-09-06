from datetime import datetime
from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number
from utils import get_rank


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "leaderboard",
                "category": "core",
                "aliases": ["lb", "ranks"],
                "description": {
                    "content": "View global or group leaderboard based on EXP.",
                    "usage": "<global|local>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        mode = contex.text.strip().lower() if contex.text else "global"
        if mode not in ("global", "local"):
            return self.client.reply_message(
                "❌ Please specify a valid leaderboard type: *global* or *local*",
                M,
            )

        try:
            users = []
            if mode == "global":
                users = list(self.client.db.models["user"].objects.all())
            else:
                participant_ids = [clean_number(p.JID.User) for p in M.group.Participants]
                users = list(
                    self.client.db.models["user"].objects.raw(
                        {"number": {"$in": participant_ids}}
                    )
                )

            if not users:
                return self.client.reply_message(
                    f"⚠ No users found for the *{mode}* leaderboard.", M
                )

            users.sort(key=lambda u: u.exp, reverse=True)
            lines = []
            now = datetime.now()
            for idx, user in enumerate(users[:10], 1):
                contact = self.client.contact.get_contact(
                    self.client.build_jid(clean_number(user.number))
                )
                name = getattr(contact, "PushName", "Unknown")
                joined_at = user.created_at.strftime("%d-%b-%Y")
                rank = get_rank(user.exp)
                time_taken = self.client.utils.format_timedelta(
                    now - user.created_at
                )
                lines.append(
                    f"#{idx}\n👤 *Name:* {name}\n🌟 *EXP:* {user.exp}\n🎖️ *Rank:* {rank['name']} {rank['data']['emoji']}\n🗓 *Joined:* {joined_at}\n⏱ *Time Taken:* {time_taken}\n"
                )

            title = f"📊 *{'Global' if mode == 'global' else 'Group'} Leaderboard* (Top 10)"
            msg = f"{title}\n\n" + "\n".join(lines)
            self.client.reply_message(msg.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Something went wrong while fetching leaderboard.", M
            )
            self.client.log.error(f"[LeaderboardError] {e}")
