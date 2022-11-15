from os import getenv

from dotenv import load_dotenv

from disnake import Intents
from disnake import Embed


from disnake.ext.commands import when_mentioned
from disnake import ApplicationCommandInteraction
from discord_util.admin.select_registered import select_registered_members

from discord_util.interactions.embeds import bot_shutdown

from discord_util.discord_static import MyClient

from sql.sql_manager import DBConnect
from sql.sql_queries import *

from discord_util.admin.update_discord_members import update_discord_members
from discord_util.admin.update_scusers import update_scsusers
from discord_util.admin.update_org import update_org

from support.create_db import create_db

def main():
    load_dotenv()

    GUILD = int(getenv("DISCORD_GUILD"))
    
    # setup intents for bot permissions
    intents = Intents.default()
    intents.members = True
    intents.presences = True

    # disable prefix in favor of just using slash commands
    # still allows for the bot to be mentioned to invoke a command if its valid
    prefix = when_mentioned

    # this is the discord bot object
    bot = MyClient(command_prefix=prefix, intents=intents)
    

    # below are all of the commands for the bot
    # default_member_permissions=8 is the same as saying only available to admins
# ADMIN COMMANDS =========================================================================================
    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def update_database_discordmembers(interaction: ApplicationCommandInteraction):
        """updates the discordmembers sql table"""
        await interaction.response.defer(with_message=True, ephemeral=True)
        members_added = await update_discord_members(interaction)
        await interaction.followup.send(f"**Task Complete**\nMembers Added: `{members_added}`")


    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def update_database_orgmembers(interaction: ApplicationCommandInteraction, sid: str):
        """updates the orgmembers sql table"""
        await interaction.response.defer(with_message=True, ephemeral=True)
        update_scsusers(interaction, sid)
        await interaction.followup.send(f"**Task Complete**")


    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def update_database_org(interaction: ApplicationCommandInteraction, sid: str):
        """updates the org sql table"""
        await interaction.response.defer(with_message=True, ephemeral=True)
        update_org(interaction, sid)
        await interaction.followup.send(f"**Task Complete**")


    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def test_registered_members(interaction: ApplicationCommandInteraction, sid: str, public = False):
        """dgfxdfg"""
        await interaction.response.defer(with_message=True, ephemeral=(not public))
        query_results = select_registered_members(interaction, sid)
        embed = Embed(title=f"registered members of {sid}", description="a description here")
        member_string = ""
        print(query_results)
        if len(query_results) > 0:
            last = query_results[0][2]
            for entry in query_results:
                org = entry[2]
                stars = entry[5] * "⭐"
                blk_squares = (5 - entry[5]) * "⬛"

                if org == last:
                    member_string += "{}{} `{: ^20}` `{: ^20}` `{}`\n".format(
                        blk_squares, stars, entry[4], entry[1], entry[6].strftime("%m/%d/%Y")
                    )

                else:
                    embed.add_field(name=last, value=member_string, inline=False)
                    member_string = "{}{} `{: ^20}` `{: ^20}` `{}`\n".format(
                        blk_squares, stars, entry[4], entry[1], entry[6].strftime("%m/%d/%Y")
                    )
                    last = entry[2]
            if sid != "all":
                embed.add_field(name=last, value=member_string, inline=False)
            await interaction.followup.send(embed=embed, ephemeral=(not public))
        else:
            await interaction.followup.send("Nothing found", ephemeral=(not public))



    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def kill(interaction: ApplicationCommandInteraction):
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(embed=bot_shutdown(interaction))
        await interaction.client.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME


# @everyone COMMANDS ======================================================================================
    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def run_sql(interaction: ApplicationCommandInteraction):
        """tests """
        await interaction.response.defer(with_message=True, ephemeral=True)
        await interaction.followup.send(f"**Task Complete**")

# REGISTERED COMMANDS =====================================================================================


# START THE BOT ===========================================================================================
    # start the bot loop
    bot.run(getenv("DISCORD_TOKEN"))


def display_title():
    name = getenv("APP_NAME")
    version = getenv("APP_VERSION")
    app_title = f" {name} Discord Bot  v.{version} "
    app_display = f"""
{'=' * (len(app_title) + 8)}
    {app_title}
{'=' * (len(app_title) + 8)}
made by {getenv("APP_CREATOR")}
"""
    print(app_display)



if __name__ == "__main__":
    display_title()
    create_db()
    main()