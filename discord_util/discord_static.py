import disnake
from disnake.ext.commands import Bot


class MyClient(Bot):


    async def on_ready(self):
        print("Connected to:")
        for guild in self.guilds:
            print('\t', guild.name)
        print(f'Logged on as: {self.user}')


async def get_game_emojis(client: MyClient):
    guild: disnake.Guild = await client.fetch_guild(1004866053043667007)
    emoji_list = {}
    for emoji in guild.emojis:
        emoji_list[emoji.name] = emoji
    return emoji_list