from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import os
import time
import check_path


def collect_match_id(tier, headers):
    """ """
    # puuid league entries들이 저장된 경로
    puuid_league_entries_path = f"./data/{tier}/puuid_league_entries"
    # match id들을 저장할 경로
    match_ids_path = f"./data/{tier}/match_ids"
    check_path.check_path(match_ids_path)
    divisions = ["I", "II", "III", "IV"]
    for division in divisions:
        puuid_league_entries_division_path = puuid_league_entries_path + "/" + division
        match_ids_division_path = match_ids_path + "/" + division
        puuid_league_entries_division_list = os.listdir(puuid_league_entries_division_path)
        for puuid_json_name in puuid_league_entries_division_list:
            puuid_league_entry_json_path = (
                puuid_league_entries_division_path + "/" + puuid_json_name
            )
            page = []
            with open(puuid_league_entry_json_path, "r") as f:
                puuid_league_entry_json = json.load(f)
                for idx, summoner in enumerate(puuid_league_entry_json):
                    puuid = summoner["puuid"]
                    MATCHID_URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30",
    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "",
}
matchId_store_path = "./silver/matchIds"
try:
    if not os.path.exists(matchId_store_path):
        os.makedirs(matchId_store_path)
except OSError:
    print("Error: Failed to create the directory")

num = 0
# 시간 제한 부분 개선 필요
with open("./silver/league_entries_puuid/silver_1_page_puuid_1.json", "r") as f:
    silver_1_page_puuid_1 = json.load(f)
    page = []
    for summoner in silver_1_page_puuid_1:
        if num == 100:
            time.sleep(120)
            num = 0
        puuid = summoner["puuid"]
        MATCHID_URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100"
        print(MATCHID_URL)
        req = Request(MATCHID_URL, headers=headers)
        try:
            response = urlopen(req)
            matchIds = json.loads(response.read().decode("utf-8"))
            print(matchIds)
            page += matchIds
            print("Store and Wait")
            time.sleep(0.05)
            num += 1
        except URLError as e:
            if hasattr(e, "reason"):
                print("We failed to reach a server.")
                print("Reason: ", e.reason)
            elif hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: ", e.code)
    path = "silver_1_page_matchid_1"
    store_path = matchId_store_path + "/" + path + ".json"
    # 중복 게임 제거
    page = list(set(page))
    with open(store_path, "w") as outfile:
        json.dump(page, outfile)
