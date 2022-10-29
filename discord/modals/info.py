from disnake.ui import Modal
from disnake.ui import Select

from disnake import SelectOption
from disnake import ModalInteraction

from discord.interactions.embeds import race_info


class infoModal(Modal):
    def __init__(self, interaction: ModalInteraction, is_public:bool) -> None:
        self.is_ephemeral = not is_public
        components: list = [
            Select(
                custom_id=f"race-select:{interaction.author.id}",
                placeholder="Select a race",
                options=[
                    SelectOption(
                        label="The Ancients", 
                        description="The ancients use the methods from lost knowledge",
                        emoji="🔱",
                        value="The Ancients|ancients"
                    ),
                    SelectOption(
                        label="Humans", 
                        description="The Human race as it has evolved from the ancients",
                        emoji="🔰",
                        value="Humans|human"
                    ),
                    SelectOption(
                        label="The Spore", 
                        description="Evolved from the depths They now walk the surface",
                        emoji="⚜️",
                        value="The Spore|spore"
                    )
                ]
            ),
            Select(
                custom_id=f"catagory-select:{interaction.author.id}",
                placeholder="Select a Catagory",
                options=[
                    SelectOption(
                        label="General Info", 
                        description="Display General information for the selected race.",
                        emoji="📝"
                    ),
                    SelectOption(
                        label="Structures", 
                        description="Display a list of Structures for the selected race.",
                        emoji="🏗️"
                    ),
                    SelectOption(
                        label="Units", 
                        description="Display a list of Units for the selected race.",
                        emoji="🪖"
                    ),
                    SelectOption(
                        label="Research", 
                        description="❌ Not Available Yet! ❌",
                        emoji="🧪"
                    )
                ]
            )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    
    async def callback(self, interaction: ModalInteraction) -> None:
        await interaction.response.send_message(embed=race_info(interaction), ephemeral=self.is_ephemeral)
