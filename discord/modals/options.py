import disnake

from discord.discord_static import get_game_emojis

class optionsModal(disnake.ui.Modal):
    def __init__(self, inter, bot) -> None:
        self.bot = bot
        components: list = [
            disnake.ui.Select(
                custom_id="Option",
                placeholder="Select a catagory",
                options=["Commands", "Buildings", "Research"]
            )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        option: str = interaction.data["components"][0]["components"][0]["values"][0]

        if option == "Commands":
            await interaction.response.send_message(content="Commands")
        elif option == "Buildings":
            await interaction.response.send_message(content="Buildings")
        elif option == "Research":
            await interaction.response.send_message(content="Research")
