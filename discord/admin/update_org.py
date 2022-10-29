from disnake import ApplicationCommandInteraction
from sql.sc_requests import SCRequester


async def update_org(interaction: ApplicationCommandInteraction):
    await interaction.response.defer(ephemeral=True)
    scr = SCRequester()
    scr.request_roster("MUNINNSOL")
    scr.request_org("MUNINNSOL")
    await interaction.followup.send("Done!\nThe roster is now up to date")