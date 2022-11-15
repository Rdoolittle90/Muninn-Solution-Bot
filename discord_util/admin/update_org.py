import mysql.connector
import requests

from json import loads as load_json
from os import getenv

from disnake import Member
from disnake import Interaction

from sql.sql_manager import DBConnect

BASE_URL = "http://api.starcitizen-api.com/"

def update_org(interaction: Interaction, SID: str):
    print("Updating org: ", SID)
    # reconnect to db using DBConnect
    conn = mysql.connector.connect(
            host = getenv("SQL_HOST"),
            user = getenv("SQL_USER"),
            passwd = getenv("SQL_PASSWORD"),
            database = getenv("SQL_DB")
            )
    c = conn.cursor()


    org_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('SC_API_KEY')}/v1/live/organization/{SID}")
    org: dict = load_json(org_request.content)["data"]

    # sql insert format
    insert_sql = """
    INSERT INTO orgs 
    (SID, Name, Logo, URL, MemberCount, IsRecruiting, IsRoleplay, PrimaryFocus, SecondaryFocus, CommitmentLevel) 
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    MemberCount = %s,
    IsRecruiting = %s
    """

    org_info = (
        SID,
        org["name"],
        org["logo"],
        org["href"],
        org["members"],
        org["recruiting"],
        org["roleplay"],
        org["focus"]["primary"]["name"],
        org["focus"]["secondary"]["name"],
        org["commitment"],
        org["members"],
        org["recruiting"]
    )
    c.execute(insert_sql, org_info)

    # finalize the transaction
    conn.commit()
    c.close()
    conn.close()

    return org["members"]