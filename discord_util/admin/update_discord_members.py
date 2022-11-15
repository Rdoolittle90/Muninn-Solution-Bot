import mysql.connector
from os import getenv

from disnake import Member
from disnake import Interaction
from disnake.errors import Forbidden

from sql.sql_manager import DBConnect


async def update_discord_members(interaction: Interaction):
    # reconnect to db using DBConnect
    conn = mysql.connector.connect(
            host = getenv("SQL_HOST"),
            user = getenv("SQL_USER"),
            passwd = getenv("SQL_PASSWORD"),
            database = getenv("SQL_DB")
            )
    c = conn.cursor()


    # sql insert format
    insert_sql = """
    INSERT INTO 
        discordusers 
            (DUID, Name, Nick, Image) 
        VALUES 
            (%s, %s, %s, %s) 
    ON DUPLICATE KEY UPDATE
        Nick = %s,
        Image = %s
    """
    

    members_added = 0  # tracks the number of members succefully added
    for member in interaction.guild.members:
        member: Member = member

        # member.nick and member.avatar may be None 
        if member.nick is None:
            member_nick = member.name
        else:
            member_nick = member.nick
            
        if member.avatar is None:
            member_avatar = member.default_avatar.url
        else:
            member_avatar = member.avatar.url

        # gathering the variables to insert                              , ON DUPLICATE
        member_info = (member.id, member.name, member_nick, member_avatar, member_nick, member_avatar)
        c.execute(insert_sql, member_info)
        members_added += 1

    # finalize the transaction
    conn.commit()
    c.close()
    conn.close()

    # Return the number of members added to the db
    return members_added