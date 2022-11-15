from disnake.ui import Modal
from disnake.ui import Select
from disnake.ui import TextInput

from disnake import SelectOption
from disnake import ModalInteraction

from os import getenv
from dotenv import load_dotenv

from discord_util.interactions.embeds import embed_members
from discord_util.discord_static import MyClient
from sql.sql_manager import DBConnect

load_dotenv()

class rosterModal(Modal):
    def __init__(self, bot: MyClient, is_public:bool) -> None:
        self.bot = bot
        self.home_sid = getenv("HOME_ORG_SID")
        self.sql = DBConnect()
        self.is_ephemeral = not is_public
        self.ranks = self.sql.select_muninn_ranks()


        ranks_options = [
            SelectOption(label="All", description="Show Everyone on the roster", value="all")
            ]
        ranks_options += [
            SelectOption(label=str(i)) for i in self.ranks
            ]

        components: list = [
            Select(
                custom_id=f"Rank",
                placeholder="Display by Rank",
                options=ranks_options
            )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    
    async def callback(self, interaction: ModalInteraction) -> None:
        option: str = interaction.data["components"][0]["components"][0]["values"][0]
        guild = self.sql.select_org(self.home_sid)
        members = self.sql.select_muninn_members(option)
        await interaction.send(content="᲼", ephemeral=self.is_ephemeral)
        await embed_members(interaction, self.bot, guild, members)
