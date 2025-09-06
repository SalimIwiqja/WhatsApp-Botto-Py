from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number
from utils import get_rank


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "whoami",
                "category": "core",
                "aliases": ["profile"],
                "description": {
                    "content": "Display user's information.",
                    "usage": "<@mention>",
                },
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            target = M.quoted_user or (
                M.mentioned[0] if M.mentioned else M.sender
            )
            target_number = clean_number(target.number)
            jid = self.client.build_jid(target_number)
            username = target.username

            user = self.client.db.get_user_by_number(target_number)
            rank = get_rank(user.exp)

            try:
                bio = self.client.get_user_info(jid)[0].UserInfo.Status
            except Exception:
                bio = "None"

            try:
                pfp_url = self.client.get_profile_picture(jid).URL
            except Exception:
                pfp_url = "https://www.pngall.com/wp-content/uploads/5/Profile-PNG-File.png"

            ban_info = ""
            if user.ban:
                ban_info = (
                    f"\n\n📝 *Reason:* {user.reason}"
                    f"\n⏰ *Banned At:* {user.banned_at.strftime('%d %b %Y, %I:%M %p')}"
                )

            message = (
                f"👤 *User Profile* 👤\n\n"
                f"📛 *Username:* {username}\n\n"
                f"📱 *Number:* {target_number}\n\n"
                f"💬 *Bio:* {bio}\n\n"
                f"🎖️ *Rank:* {rank['name']} {rank['data']['emoji']}\n\n"
                f"✨ *EXP:* {user.exp}\n\n"
                f"📅 *Joined On:* {user.created_at.strftime('%d %b %Y, %I:%M %p')}\n\n"
                f"{'🚫 *Status:* Banned' + ban_info if user.ban else '✅ *Status:* Active'}\n\n"
                f"(Use *{self.client.config.prefix}rank* to see ranks and more user info.)"
            )

            self.client.send_image(
                M.gcjid,
                self.client.utils.fetch_buffer(pfp_url),
                caption=message,
                quoted=M,
            )

        except Exception as e:
            self.client.reply_message("❌ Failed to retrieve profile.", M)
            self.client.log.error(f"[whoami] {e}")
