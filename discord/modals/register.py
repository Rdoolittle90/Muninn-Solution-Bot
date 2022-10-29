import asyncio
import disnake
from disnake import Embed
from disnake import Color

from discord.discord_static import MyClient, get_game_emojis
from sql.sc_requests import SCRequester
from settings import *



class  registerModal(disnake.ui.Modal):
    def __init__(self, interaction: disnake.ModalInteraction, bot: MyClient) -> None:
        self.bot = bot
        self.scr = SCRequester()
        self.role_dict = {}
        self.guild = bot.get_guild(914043475891208262)

        self.testers = ["Iban Blast"]

        for role in self.guild.roles:
            self.role_dict[role.name] = role.id

        components: list = [
            disnake.ui.TextInput(
                    label="Enter your Star Citizen handle",
                    placeholder="",
                    custom_id=f"register_{interaction.author.id}",
                    min_length=5,
                    max_length=20,
                    required=True
                )
        ]
        super().__init__(title="Link your Star Citizen Display name", components=components)

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        
        await interaction.response.defer(ephemeral=True)
        self.scr.request_roster("MUNINNSOL")
        org_members = self.scr.sql.select_org_members()
        option: str = interaction.data["components"][0]["components"][0]["value"]
        registered = self.scr.sql.select_registered()
        select_pid = self.scr.sql.select_pid(interaction.author.id)
        info = self.scr.sql.select_member_by_Handle(option)
        for member in org_members:
            if option.lower() == member[4].lower():
                found = True
                break
            else:
                found = False
        if found == True:
            if option.lower() in registered:
                await interaction.followup.send(content="Account already Registered", ephemeral=True)
            elif len(select_pid) > 0:
                await interaction.followup.send(content="Account already Registered", ephemeral=True)
            else:
                
                trying = True
                while trying:

                    try:
                        self.scr.sql.update_member(option, interaction.author.id)
                        self.scr.sql.conn.commit()
                        trying = False
                    except Exception as e:
                        print(e)
                        await asyncio.sleep(1)

                try:
                    await interaction.author.edit(nick = self.scr.sql.select_display_name(interaction.author.id))
                    await interaction.author.remove_roles(self.guild.get_role(1009527562931818576))
                
                    rsi_handle = self.scr.sql.select_pid(interaction.author.id)
                    rsi_rank = self.scr.sql.select_member_by_Handle(rsi_handle[0][0])[6]
                    role_id = self.role_dict[rsi_rank]
                    new_role = self.guild.get_role(role_id)

                    await interaction.author.add_roles(new_role)

                    if interaction.author.name in self.testers:
                        print(f"Access 3 granted to {interaction.author.name}")
                        await interaction.author.add_roles(self.guild.get_role(1007072739351351458))

                    if new_role.name in ACCESS_1:
                        print(f"Access 3 granted to {interaction.author.name}")
                        await interaction.author.add_roles(self.guild.get_role(1007072739351351458))
                    
                    if new_role.name in ACCESS_2:
                        print(f"Access 2 granted to {interaction.author.name}")
                        await interaction.author.add_roles(self.guild.get_role(1007070395863674900))
                    
                    if new_role.name in ACCESS_1:
                        print(f"Access 1 granted to {interaction.author.name}")
                        await interaction.author.add_roles(self.guild.get_role(1007071862259449927))

                        
                except disnake.errors.Forbidden as e:
                    print(e, "---", interaction.author)

                except TypeError as e:
                    print(e, "---", interaction.author)

                embed = disnake.Embed(
                    title="Account Registered",
                    description="You will now have access to new commands",
                    color = disnake.Color.green()
                )
                if info[5] != None:
                    embed.set_thumbnail(url=info[5])
                embed.add_field(name="Rank", value=info[6], inline=True)
                embed.add_field(name="Display Name", value=info[3], inline=True)
                embed.add_field(name="Organization", value=info[2], inline=True)

                await interaction.followup.send(embed=embed)
        else:
            embed = Embed(title="Handle Not Found", description="Potential Reasons", url="https://robertsspaceindustries.com/orgs/MUNINNSOL")
            embed.add_field(
                name="Register On RSI",
                value="""
                Please double check that your Org application has been accepted.
                if you have not applied you can do so here: https://robertsspaceindustries.com/orgs/MUNINNSOL
                """,
                inline=False
            )
            embed.add_field(
                name="Check Spelling",
                value=f"did you mean to type:\n`{option}`",
                inline=False
            )
            embed.set_thumbnail(
                self.guild.icon.url
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)

            channel = self.guild.get_channel(915069773493198868)
            await channel.send(f"A Registration error occurred\n{option} was not found in the roster")