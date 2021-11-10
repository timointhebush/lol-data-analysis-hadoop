from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import os
import time

PUUID_LEAGUE_ENTRIES_URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30",
    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "",
}
base_store_path = "./silver/league_entries_puuid"
try:
    if not os.path.exists(base_store_path):
        os.makedirs(base_store_path)
except OSError:
    print("Error: Failed to create the directory")

num = 0
# 시간 제한 부분 개선 필요
with open("./silver/silver_1_page_1.json", "r") as f:
    silver_1_page_1_json = json.load(f)
    path = "silver_1_page_puuid_1"
    page = []
    for summoner in silver_1_page_1_json:
        if num == 100:
            time.sleep(120)
            num = 0
        summonerId = summoner["summonerId"]
        summonerName = summoner["summonerName"]
        LEAGUE_ENTRIES_URL = PUUID_LEAGUE_ENTRIES_URL + summonerId
        req = Request(LEAGUE_ENTRIES_URL, headers=headers)
        try:
            response = urlopen(req)
            summoner_puuid = json.loads(response.read().decode("utf-8"))
            print(summoner_puuid)
            page += [summoner_puuid]
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
    store_path = base_store_path + "/" + path + ".json"
    with open(store_path, "w") as outfile:
        json.dump(page, outfile)
