from disnake import ApplicationCommandInteraction

from discord_util.interactions.embeds import private_stats
from discord_util.interactions.embeds import public_stats


async def display_public_player_stats(interaction: ApplicationCommandInteraction, pid: int) -> None:
    content = None
    if interaction.author.id != pid:
        content = f"<@{pid}>"
    await interaction.response.send_message(content=content, embed=public_stats(interaction, pid))

async def display_private_player_stats(interaction: ApplicationCommandInteraction) -> None:
    await interaction.send(embed=private_stats(interaction), ephemeral=True)
    