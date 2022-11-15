import disnake
from disnake import TextInputStyle

from discord_util.discord_static import get_game_emojis
from sql.sql_manager import extraDBConnect

class insertPoemModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components: list = [
            disnake.ui.TextInput(
                label="Title", 
                custom_id="title_id",
                style=TextInputStyle.short,
                required=True,
                max_length=15
                ),
            disnake.ui.TextInput(
                label="Author", 
                custom_id="author_id",
                style=TextInputStyle.short,
                required=False,
                max_length=15,
                value="Unknown"
                ),
            disnake.ui.TextInput(
                label="Poem", 
                custom_id="poen_id",
                style=TextInputStyle.paragraph,
                required=True
                )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        title: str = interaction.data["components"][0]["components"][0]["value"]
        author: str = interaction.data["components"][1]["components"][0]["value"]
        poem: str = interaction.data["components"][2]["components"][0]["value"]

        sql: extraDBConnect = extraDBConnect()
        sql.insert_poems(title, author, poem)
        sql.c.connection.commit()
        sql.c.connection.close()
        await interaction.send("Done!")

