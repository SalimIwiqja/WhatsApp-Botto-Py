from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "groupinfo",
                "category": "core",
                "aliases": ["ginfo"],
                "description": {
                    "content": "Displays detailed info about the current group."
                },
                "group": True,
                "exp": 4,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            group_info = M.group
            gcjid_number = clean_number(M.gcjid.User)
            group_data = self.client.db.get_group_by_number(gcjid_number)

            try:
                pfp_url = self.client.get_profile_picture(M.gcjid.User).URL
            except Exception:
                pfp_url = "https://www.pngall.com/wp-content/uploads/5/Profile-PNG-File.png"

            subject = group_info.GroupName.Name if group_info.GroupName else "N/A"
            description = group_info.GroupTopic.Topic if group_info.GroupTopic.Topic else "N/A"
            participants = group_info.Participants or []
            admins = self.client.filter_admin_users(participants)
            admin_count = len(admins)
            total_members = len(participants)

            events_status = "Enabled" if group_data.events else "Disabled"
            mod_status = "Enabled" if group_data.mod else "Disabled"

            caption = f"""
🏷️ *Group Subject:* {subject}

🎖️ *Admins:* {admin_count}

📋 *Total Members:* {total_members}

🍃 *Events:* {events_status}

⚡ *Mods:* {mod_status}

🌌 *Description:*
{description}
            """.strip()

            image_msg = self.client.build_image_message(
                self.client.utils.fetch_buffer(pfp_url),
                caption=caption,
                quoted=M,
            )
            self.client.send_message(M.gcjid, message=image_msg)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to get group information.", M)
            self.client.log.error(f"[groupinfo] {e}")
