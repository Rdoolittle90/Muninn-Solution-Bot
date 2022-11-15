import random
from disnake import Embed
from disnake import Color
from disnake import ApplicationCommandInteraction
from datetime import date, datetime

from sql.sql_manager import DBConnect


# async def display_user(interaction: ApplicationCommandInteraction, name: str):
#     await interaction.response.defer(ephemeral=True)
#     if name == None:
#         name = interaction.author.nick
#     sql = SCRequester()
#     member = sql.request_member(name)
#     print(member)
#     if member:
#         enlisted = member['profile']['enlisted'].split("T")[0].split("-")
#         d0 = date(int(enlisted[0]), int(enlisted[1]), int(enlisted[2]))
#         d1 = date.today()
#         delta: date = d1 - d0
#         stars = '⭐' * member["organization"]["stars"]
#         if len(member["organization"].keys()) > 1:
#             embed = Embed(
#                     title=member["profile"]["display"],
#                     description=stars,
#                     url=member["profile"]["page"]["url"]
#             )
#             embed.set_author(
#                 name=member["organization"]["name"],
#                 url=f"https://robertsspaceindustries.com/orgs/{member['organization']['sid']}",
#                 icon_url=member["organization"]["image"]
#             )
#         else:
#             embed = Embed(
#                     title=member["profile"]["display"],
#                     description="No listed Orgs",
#                     url=member["profile"]["page"]["url"]
#             )

#         embed.set_thumbnail(url=member["profile"]["image"])

#         embed.add_field(name="Enlisted", value=f"`{delta.days}` days ago", inline=True)
#         languages = "\n".join(member["profile"]["fluency"])

#         embed.add_field(name="Fluency", value=languages, inline=True)
#         if "bio" in member["profile"].keys():
#             embed.add_field(name="Bio", value=member["profile"]["bio"], inline=False)
#     else:
#         embed = Embed(
#             title=f"Player Not Found `{name}`",
#             description="check spelling *(it should match thier ingame name)*"
#         )

#     await interaction.followup.send(embed=embed)

# def display_poem():
#     sql = extraDBConnect()
#     poems = sql.select_poems()
#     print(poems)
#     poem = random.choice(poems)
#     embed = Embed(
#         title=poem[1],
#         description=f"by: {poem[2]}"
#     )
#     embed.add_field(
#         name="<—  —  —>",
#         value=poem[3]
#     )
#     return embed


def bot_shutdown(interaction: ApplicationCommandInteraction):
    embed = Embed(
        title="Shutting Down",
        description=f"Bot kill command executed by {interaction.author}",
        color=Color.red()
    )
    return embed

# def display_recent_change_report(interaction: ApplicationCommandInteraction) -> None:
#     embed = Embed(
#         title="Recent Changes - {}"
#     )

# async def embed_members(interaction, bot, guild, members):
#     size = 25

#     if len(members) < size:
#         embed = Embed(
#             title=f"Member Roster [`{guild[4]}`]",
#             description=f"**SID**: `{guild[1]}`",
#             color=Color.dark_gold()
#         )
#         embed.set_author(
#             name="Muninn Solutions",
#             url=guild[6],
#             icon_url=guild[5]
#         )
#         embed.set_thumbnail(
#             url=guild[5]
#         )
#         member_str = ""
#         for member in members:
#             stars = '⭐' * member[7]
#             blk_sqr = '⬛' * (5 - member[7])
#             member_str += f"{blk_sqr}{stars} `{member[6]}` **{member[3]}**\n"
        
#         embed.add_field(
#             name="᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼Rank - Name",
#             value=member_str
#         )
#         await interaction.send(embed=embed)
#     else:
#         page_strs = []
#         member_str = ""
#         for i, member in enumerate(members):
#             stars = '⭐' * member[7]
#             blk_sqr = '⬛' * (5 - member[7])
#             member_str += f"{blk_sqr}{stars} `{member[6]}` **{member[3]}**\n"
#             if i % size == 0 and i > 0:
#                 print(member_str)
#                 page_strs.append(member_str)
#                 member_str = ""
#         page_strs.append(member_str)
        
#         pages = []
#         for i, v in enumerate(page_strs):
#             embed = Embed(
#             title=f"Member Roster [`{guild[4]}`]",
#             description=f"**SID**: `{guild[1]}`",
#             color=Color.dark_gold()
#             )
#             embed.set_author(
#                 name="Muninn Solutions",
#                 url=guild[6],
#                 icon_url=guild[5]
#             )
#             embed.set_thumbnail(
#                 url=guild[5]
#             )
#             embed.add_field(
#                 name="᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼Rank - Name",
#                 value = v
#             )
#             embed.set_footer(text=f"Page: {i + 1}/{len(page_strs)}")
#             pages.append(embed)
#         message = await bot.get_channel(interaction.channel_id).send(embed = pages[0])
#         await message.add_reaction('⏮')
#         await message.add_reaction('◀')
#         await message.add_reaction('▶')
#         await message.add_reaction('⏭')

#         def check(reaction, user):
#             return user == interaction.author

#         i = 0
#         reaction = None
#         while True:
#             if str(reaction) == '⏮':
#                 i = 0
#                 await message.edit(embed = pages[i])
#             elif str(reaction) == '◀':
#                 if i > 0:
#                     i -= 1
#                     await message.edit(embed = pages[i])
#             elif str(reaction) == '▶':
#                 if i < len(pages) - 1:
#                     i += 1
#                     await message.edit(embed = pages[i])
#             elif str(reaction) == '⏭':
#                 i = len(pages) - 1
#                 await message.edit(embed = pages[i])
            
#             try:
#                 reaction, user = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
#                 await message.remove_reaction(reaction, user)
#             except:
#                 break

#         await message.clear_reactions()


# def embedder(interaction: ApplicationCommandInteraction, title: str, disc: str, info: str, time: str):
#     year, month, day, hour, minutes = time.split("-")
#     preset_date = datetime(int(year), int(month) + 1, int(day), int(hour), int(minutes))

#     embed = Embed(
#         title=title,
#         description=disc,
#         timestamp=datetime.today()
#     )
#     embed.set_author(
#         name=interaction.author.nick,
#         icon_url=interaction.author.display_avatar.url
#     )
#     embed.set_thumbnail(
#         url=interaction.guild.icon.url
#     )
#     embed.add_field(
#         name="Event Details",
#         value=info,
#         inline=False
#     )
#     embed.add_field(
#         name=f"Event Time: <t:{int(preset_date.timestamp())}:F>",
#         value=f"<t:{int(preset_date.timestamp())}:R>"
#     )

#     return embed