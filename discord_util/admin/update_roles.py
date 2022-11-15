import random
from disnake import ApplicationCommandInteraction
from disnake.errors import Forbidden

from discord_util.discord_static import MyClient
from sql.sql_manager import DBConnect
from settings import *


async def update_roles(interaction: ApplicationCommandInteraction, bot: MyClient):

    access_1 = ["Associate", "Senior Associate", "Night Raven Original"]
    access_2 = ["Manager", "Director"]
    access_3 = ["Board Member"]

    await interaction.response.defer(ephemeral=True)
    sql = DBConnect()
    registered_ids = sql.select_registered_ids()
    members = bot.get_all_members()

    guild = bot.get_guild(914043475891208262)

    role_dict = {}
    for role in guild.roles:
        role_dict[role.name] = role.id

    for member in members:
        try:
            if member.bot:
                continue
            if member.id not in registered_ids:
                for role in member.roles:
                    if role.name != "@everyone":
                        await member.remove_roles(role)
                    await member.add_roles(guild.get_role(1009527562931818576))
            else:
                for role in member.roles:
                    if role.name not in IGNORE_ROLES:
                        await member.remove_roles(role)
                
                rsi_handle = sql.select_pid(member.id)
                rsi_rank = sql.select_member_by_Handle(rsi_handle[0][0])[6]
                role_id = role_dict[rsi_rank]
                new_role = guild.get_role(role_id)

                await member.add_roles(new_role)

                if member.name in TESTERS:
                    print(f"Access 3 granted to {member.name}")
                    await member.add_roles(guild.get_role(1007072739351351458))
                    await member.remove_roles(guild.get_role(1009527562931818576))

                if new_role.name in access_3:
                    print(f"Access 3 granted to {member.name}")
                    await member.add_roles(guild.get_role(1007072739351351458))
                
                if new_role.name in access_2:
                    print(f"Access 2 granted to {member.name}")
                    await member.add_roles(guild.get_role(1007070395863674900))
                
                if new_role.name in access_1:
                    print(f"Access 1 granted to {member.name}")
                    await member.add_roles(guild.get_role(1007071862259449927))

        except Forbidden as ex:
            print("====================")
            print(member.name)
            print(ex.text)
            print("====================")

    await interaction.followup.send(content="Job Done")