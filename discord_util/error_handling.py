from disnake.errors import NotFound
from disnake.errors import Forbidden

from disnake.ext.commands.errors import MissingPermissions


def error_handling(interaction, e):
    if isinstance(e, MissingPermissions):
        print(f"[Missing Permissions] {interaction.author} has DMs disabled.")
    elif isinstance(e, NotFound):
        print(f"[Not Found] message was likely deleted")
    else:
        raise(e)