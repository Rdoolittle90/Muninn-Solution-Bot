from datetime import datetime, timezone, tzinfo
import disnake
from disnake import TextInputStyle
from disnake import DMChannel
from disnake import ApplicationCommandInteraction
from discord_util.discord_static import get_game_emojis
from discord_util.interactions.embeds import embedder
from sql.sql_manager import extraDBConnect


class embedderModal(disnake.ui.Modal):
    def __init__(self, interaction: ApplicationCommandInteraction) -> None:
        utcshift = -6
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        hour = datetime.now().hour
        minute = datetime.now().minute
        second = datetime.now().second

        default_info = """All the `info` anyone will need for the event
        this can be multi-line and include the discord
        word tags like **bold** or strike ~~strike~~
        ```python\nstring = "it can even include formated code blocks"```
        """

        components: list = [
            disnake.ui.TextInput(
                label=f"Title", 
                custom_id="title",
                style=TextInputStyle.short,
                required=True,
                max_length=30,
                value="Event Name"
                ),
            disnake.ui.TextInput(
                label="Desription", 
                custom_id="disc",
                style=TextInputStyle.short,
                required=False,
                max_length=45,
                value="an awesome event is going to happen"
                ),
            disnake.ui.TextInput(
                label="event info", 
                custom_id="event_info",
                style=TextInputStyle.paragraph,
                required=True,
                value=default_info
                ),
            disnake.ui.TextInput(
                label="event time [yyyy-mm-dd-hh-mm]", 
                custom_id="event_time_id",
                style=TextInputStyle.paragraph,
                required=True,
                value=f"{year}-{month}-{day}-{hour}-{minute}"
                )
        ]
        super().__init__(title="Setup an event embed", components=components)
    
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        title:str = interaction.data["components"][0]["components"][0]["value"]
        disc: str = interaction.data["components"][1]["components"][0]["value"]
        info: str = interaction.data["components"][2]["components"][0]["value"]
        time: str = interaction.data["components"][3]["components"][0]["value"]

        dm_channel: DMChannel  = await interaction.bot.create_dm(interaction.author)
        await dm_channel.send(embed=embedder(interaction, title, disc, info, time))
        await interaction.response.send_message("Check your DMs does the embed look correct?", ephemeral=True)
        