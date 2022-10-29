from os import getenv

from dotenv import load_dotenv

from discord import Intents
from discord.ext.commands import when_mentioned
from discord import ApplicationCommandInteraction

from discord.interactions.embeds import bot_shutdown
from discord.interactions.embeds import display_funds
from discord.interactions.embeds import display_org
from discord.interactions.embeds import display_poem
from discord.interactions.embeds import embed_members
from discord.interactions.embeds import display_user

from discord.admin.update_roles import update_roles as ms_update_roles
from discord.admin.update_nicks import update_nicks as ms_update_nicks
from discord.admin.update_org import update_org as ms_update_org

from discord.error_handling import error_handling

from discord.modals.embedder import embedderModal
from discord.modals.insertPoem import insertPoemModal
from discord.modals.register import registerModal

from discord.discord_static import MyClient

from sql.sql_manager import DBConnect


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
    async def update_nicks(interaction: ApplicationCommandInteraction):
        """Admin command tp update all users nicknames to match their SC Handle"""
        await ms_update_nicks(interaction, bot)

    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def update_roles(interaction: ApplicationCommandInteraction):
        """Admin Command to update all users roles to match the SC Roster"""
        await ms_update_roles(interaction, bot)

    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def update_org(interaction: ApplicationCommandInteraction):
        """Admin Command to update the org details"""
        await ms_update_org(interaction)
    
    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def event_embed(interaction: ApplicationCommandInteraction):
        """create an event embed testing"""
        await interaction.response.send_modal(modal=embedderModal(interaction))

    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def add_poem(interaction: ApplicationCommandInteraction):
        """adds a poem to the extras db"""
        await interaction.response.send_modal(modal=insertPoemModal())

    @bot.slash_command(guild_ids=[GUILD], default_member_permissions=8)
    async def kill(interaction: ApplicationCommandInteraction):
        """
            Kill the bot ending the program, requires manual reboot
        """
        await interaction.send(embed=bot_shutdown(interaction))
        await interaction.client.close()

# @everyone COMMANDS =========================================================================================

    @bot.slash_command(guild_ids=[GUILD])
    async def register(interaction: ApplicationCommandInteraction):
        """Register by linking your Star Citizen Handle to your discord id"""
        await interaction.response.send_modal(modal=registerModal(interaction, bot))

    @bot.slash_command(guild_ids=[GUILD])
    async def poem(interaction: ApplicationCommandInteraction, is_public=False):
        """displays a random poem."""
        await interaction.response.send_message(embed=display_poem(), ephemeral=not is_public)

# REGISTERED COMMANDS ====================================================================================

    @bot.slash_command(guild_ids=[GUILD])
    async def roster(interaction: ApplicationCommandInteraction, is_public: bool = False):
        """Display The Muninn Solutions Roster"""
        is_ephemeral = not is_public
        sql = DBConnect()
        await interaction.response.defer(ephemeral=is_ephemeral)
        guild = sql.select_org("MUNINNSOL")
        members = sql.select_muninn_members("all")
        await interaction.followup.send(content="᲼")
        await embed_members(interaction, bot, guild, members)

        ## this is disabled due to some bug with Select list modals
        ## if fixed move above logic into rosterModal() and uncomment then remove this note
        #await interaction.response.send_modal(modal=rosterModal(bot, is_public))

    @bot.slash_command(guild_ids=[GUILD])
    async def lookup(interaction: ApplicationCommandInteraction, handle:str = None):
        """Lookup a users player handle"""
        await display_user(interaction, handle)

    @bot.slash_command(guild_ids=[GUILD])
    async def org_lookup(interaction: ApplicationCommandInteraction, handle:str = None):
        """Lookup an org by its SID"""
        await display_org(interaction, handle)

    @bot.slash_command(guild_ids=[GUILD])
    async def funds(interaction: ApplicationCommandInteraction):
        """Display the latest report via the api on funds raised"""
        await display_funds(interaction)

# ERROR EVENT ============================================================================================

    @bot.event
    async def on_command_error(interaction, error):
        """Handle errors if possible"""
        error_handling(interaction, error)

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
    main()