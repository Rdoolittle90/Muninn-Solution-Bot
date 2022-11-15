import mysql.connector
import requests

from json import loads as load_json
from json import dump as dump_json
from os import getenv

from disnake import Member
from disnake import Interaction

from discord_util.admin.update_org import update_org
from sql.sql_manager import DBConnect


BASE_URL = "http://api.starcitizen-api.com/"


def update_scsusers(interaction: Interaction, SID: str, org_sids = []):
    # reconnect to db using DBConnect
    conn = mysql.connector.connect(
        host = getenv("SQL_HOST"),
        user = getenv("SQL_USER"),
        passwd = getenv("SQL_PASSWORD"),
        database = getenv("SQL_DB")
        )
    c = conn.cursor()

    select_from_orgs = "SELECT SID FROM orgs"

    sql_insert_into_scusers = """
    INSERT INTO scusers (Handle, Badge, Enlisted, Image)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    Image=%s
    """
    sql_select_uid = "SELECT UID FROM scusers WHERE Handle = %s"

    sql_insert_into_orgmembers = """
    INSERT INTO orgmembers (UID, SID, IsPrimary, MemberRank, Stars)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    MemberRank=%s,
    Stars=%s
    """
    org_sids.append(SID)
    update_org(interaction, SID)
    
    orgs_added = 0
    users_added = 0
    users_updated = 0

    # request the org members using the provided SID
    org_roster = {}
    page = 1
    member_count = 0
    idx = 1
    while True:
        org_roster_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('SC_API_KEY')}/v1/live/organization_members/{SID}?page={page}")
        org_roster = load_json(org_roster_request.content)["data"]
        if len(org_roster) == 0:
            break
        else:
            member_count += len(org_roster)
        
        for member in org_roster:
            user_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('SC_API_KEY')}/v1/auto/user/{member['handle']}")
            response_dict: dict = load_json(user_request.content)

            user_info = (
                member["handle"],
                response_dict["data"]["profile"]["badge"],
                response_dict["data"]["profile"]["enlisted"],
                response_dict["data"]["profile"]["image"],
                response_dict["data"]["profile"]["image"]  # used on update
                )
            c.execute(sql_insert_into_scusers, user_info)

            c.execute(sql_select_uid, (member["handle"], ))
            user_id = c.fetchone()[0]
            
            if "sid" not in response_dict["data"]["organization"].keys():
                print(f"{idx}/{member_count} No default org")
            else:
                if response_dict["data"]["organization"]["sid"] in org_sids:
                    pass
                else:
                    orgmember_info = (
                        user_id,
                        response_dict["data"]["organization"]["sid"],
                        1,
                        response_dict["data"]["organization"]["rank"],
                        response_dict["data"]["organization"]["stars"],
                        response_dict["data"]["organization"]["rank"],
                        response_dict["data"]["organization"]["stars"]
                    )
                    print(f"{idx}/{member_count}", orgmember_info[:-2])
                    update_org(interaction, response_dict["data"]["organization"]["sid"])
                    c.execute(sql_insert_into_orgmembers, orgmember_info)

            for org in response_dict["data"]["affiliation"]:
                if "sid" not in org.keys():
                    continue
                try:
                    if org["sid"] in org_sids:
                        pass
                    else:
                        org_sids.append(org["sid"])
                        update_org(interaction, org["sid"])
                    
                    orgmember_info = (
                        user_id,
                        org["sid"],
                        0,
                        org["rank"],
                        org["stars"],
                        org["rank"],
                        org["stars"]
                    )
                    print(f"{idx}/{member_count}", orgmember_info[:-2])
                    c.execute(sql_insert_into_orgmembers, orgmember_info)

                except KeyError as err:
                    with open("output.json", "w") as fout:
                        dump_json(response_dict, fout, indent=4)
            if idx % 5 == 0:
                conn.commit()
            idx += 1
        page += 1

    # finalize the transaction
    c.close()
    conn.close()

    return (users_added, orgs_added)



if __name__ == "__main__":
    user_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('SC_API_KEY')}/v1/auto/user/Nasdaqus")
    response_dict: dict = load_json(user_request.content)

    with open("output.json", "w") as fout:
        dump_json(response_dict, fout, indent=4)

    print(response_dict)
    print()