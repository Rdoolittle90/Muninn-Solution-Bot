import requests
import json
from sql.sql_manager import DBConnect

from os import getenv
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "http://api.starcitizen-api.com/"


class SCRequester():
    """A Class used to request all things star citizen using api calls"""
    def __init__(self):
        self.home_sid = getenv("HOME_ORG_SID")
        self.sql = DBConnect()

    def request_stats(self):
        """Request the current stats provided used for /funds"""
        stats_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/live/stats?")
        stats: dict = json.loads(stats_request.content)["data"]

        return stats


    def request_updates(self):
        """Request versions and category listings"""
        version_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/gamedata/list/versions?")
        version_list: dict = json.loads(version_request.content)["data"]

        category_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/gamedata/list/categories?")
        category_list: dict = json.loads(category_request.content)["data"]

        self.sql.update_versions(version_list)
        self.sql.update_categories(category_list)

        self.sql.conn.commit()

    def request_roster(self, name:str):
        """
        Request the roster of the provided org SID
        FIX NEEDED needs to have the pages added dynamically
        """
        org_roster_request1: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/live/organization_members/{name}?page=1") # this
        org_roster1: dict = json.loads(org_roster_request1.content)["data"]
        org_roster_request2: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/live/organization_members/{name}?page=2") # not good
        org_roster2: dict = json.loads(org_roster_request2.content)["data"]
        
        registered = [i[4] for i in self.sql.select_muninn_members()]

        for member in org_roster1:
            if member["handle"] in registered:
                self.sql.update_member_all(member["handle"], member)
            else:
                print(f"Insert: {member['handle']}")
                self.sql.insert_member(name, member)

        for member in org_roster2:
            if member["handle"] in registered:
                self.sql.update_member_all(member["handle"], member)
            else:
                print(f"Insert: {member['handle']}")
                self.sql.insert_member(name, member)

        self.sql.conn.commit()


    def request_org(self, name:str):
        """Request org information using the provided org SID"""
        org_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/live/organization/{name}")
        org: dict = json.loads(org_request.content)["data"]

        muninn = self.sql.select_org(getenv("HOME_ORG_SID"))
        if len(muninn) > 0:
            self.sql.update_org(org, name)
        else:
            self.sql.insert_org(org)

        self.sql.conn.commit()


    def request_member(self, name:str):
        """Request information on a specific user using their Handle"""
        user_request: requests.Response = requests.get(url=f"{BASE_URL}{getenv('API_KEY')}/v1/auto/user/{name}")
        response_dict: dict = json.loads(user_request.content)
        
        if response_dict['success'] != 1:
            print(response_dict)
            return False
        if not response_dict['data']:
            print(response_dict)
            return False
        if len(response_dict['data'].keys()) == 0:
            print(response_dict)
            return False
        
        with open(f"user_temp/{name}.json", 'w') as fout:
            json.dump(response_dict['data'], fout, indent=4)

        user: dict = json.loads(user_request.content)["data"]

        return user