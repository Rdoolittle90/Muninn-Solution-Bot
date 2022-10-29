import random
from discord import ApplicationCommandInteraction
from discord.errors import Forbidden

from discord.discord_static import MyClient
from sql.sql_manager import DBConnect

from datetime import datetime
from datetime import timedelta


def get_holiday_index():
    todays_date = datetime.today()
    todays_year = todays_date.strftime("%y")
    
    date_fmt = "%y-%m-%d"
    holidays = [
        datetime.strptime(f"{todays_year}-10-31", date_fmt).timetuple().tm_yday, # halloween
        datetime.strptime(f"{todays_year}-11-24", date_fmt).timetuple().tm_yday, # thanksgiving
        datetime.strptime(f"{todays_year}-12-25", date_fmt).timetuple().tm_yday  # christmas
    ]

    day_of_year = datetime.now().timetuple().tm_yday

    for index, holiday in enumerate(holidays):
        start = holiday - 30
        end = holiday

        if day_of_year in range(start, end):
            return index + 1
    return 0



async def update_nicks(interaction: ApplicationCommandInteraction, bot: MyClient):
    await interaction.response.defer(ephemeral=True)
    sql = DBConnect()
    registered_ids = sql.select_registered_ids()
    discord_members = bot.get_all_members()
    org_members = [i[4] for i in sql.select_muninn_members()]

    fixed = 0
    skipped = 0

    current_holiday = get_holiday_index()
    print(current_holiday)
    holiday_emojis = [
        [""],                        # 0 - Blank
        ["🎃", "🦇", "👻", "💀"],  # 1 - Halloween
        ["🦃"],                     # 2 - Thanksgiving
        ["🎄", "🎅", "🎁", "🦌"], # 3 - Christmas
        ["🎆", "🎇", "⏭️"]         # 4 - New Years
    ]

    for member in discord_members:
        emoji_to_add = random.choice(holiday_emojis[current_holiday])

        if member.name == bot.user.name:
            continue

        if member.nick == None:
            if member.get_role(1009527562931818576) != None:
                fixed += 1
                await member.edit(nick="✕ " + member.name + emoji_to_add)
            else:
                skipped += 1
                continue

        if member.nick in org_members:
            skipped += 1
            continue

        try:
            if member.id in registered_ids:
                fixed += 1
                await member.edit(nick=sql.select_handle_name(member.id) + emoji_to_add)

            else:
                await member.edit(nick="✕ " + member.name + emoji_to_add)

        except Forbidden as ex:
            print(f"[Error] setting nick for {member.nick}")

    await interaction.followup.send(content=f"Job Done\nFixed: `{fixed}`\nSkipped: `{skipped}`")


if __name__ == "__main__":
    print(get_holiday_index())