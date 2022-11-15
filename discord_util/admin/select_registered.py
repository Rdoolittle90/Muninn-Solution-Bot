import mysql.connector
import pandas as pd

from os import getenv

from disnake import Member
from disnake import Interaction
from disnake.errors import Forbidden

from sql.sql_manager import DBConnect


def select_registered_members(interaction: Interaction, sid: str):
    # reconnect to db using DBConnect
    conn = mysql.connector.connect(
            host = getenv("SQL_HOST"),
            user = getenv("SQL_USER"),
            passwd = getenv("SQL_PASSWORD"),
            database = getenv("SQL_DB")
            )
    c = conn.cursor()

    if sid == "all":
        print("no sid")
        # sql insert format
        select_all_registered = """
        SELECT 
            OM.MID, 
            SC.Handle, 
            OM.SID, 
            OM.IsPrimary, 
            OM.MemberRank, 
            OM.Stars, 
            SC.Enlisted, 
            D.Nick, 
            D.DUID, 
            D.Image
        FROM 
            orgmembers OM
                INNER JOIN 
            scusers SC ON SC.UID = OM.UID
                LEFT JOIN 
            discordusers D ON D.DUID = SC.DUID
        WHERE 
            D.DUID > 0 AND OM.IsPrimary = 1
        ORDER BY OM.SID, OM.Stars DESC, SC.Enlisted;
        """
        c.execute(select_all_registered)

    else:
        print("sid provided")
        select_registered_where_sid_var= """
        SELECT 
            OM.MID, 
            SC.Handle, 
            OM.SID, 
            OM.IsPrimary, 
            OM.MemberRank, 
            OM.Stars, 
            SC.Enlisted, 
            D.Nick, 
            D.DUID, 
            D.Image
        FROM 
            orgmembers OM
                INNER JOIN 
            scusers SC ON SC.UID = OM.UID
                LEFT JOIN 
            discordusers D ON D.DUID = SC.DUID
        WHERE 
            D.DUID > 0 AND OM.Stars >= 1 AND OM.SID = %s
        ORDER BY OM.SID, OM.Stars DESC, SC.Enlisted;
        """
        c.execute(select_registered_where_sid_var, (sid, ))
    
    query_results = c.fetchall()
    c.close()
    conn.close()

    return query_results