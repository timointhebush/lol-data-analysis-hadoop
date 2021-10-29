from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30",
    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-04da3595-378f-40c6-8d1f-3123e50a72b0",
}

store_path = "./silver/timelines"
try:
    if not os.path.exists(store_path):
        os.makedirs(store_path)
except OSError:
    print("Error: Failed to create the directory")

num = 0
# 시간 제한 부분 개선 필요
with open("./silver/matchIds/silver_1_page_matchid_1.json", "r") as f:
    JSON = json.load(f)
    for matchId in JSON:
        if num == 100:
            time.sleep(120)
            num = 0
        TIMELINE_URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline"
        print(TIMELINE_URL)
        req = Request(TIMELINE_URL, headers=headers)
        try:
            response = urlopen(req)
            timeline = json.loads(response.read().decode("utf-8"))
            print(timeline)
            print("Store and Wait")
            time.sleep(0.05)
            num += 1
            path = store_path + "/" + matchId + ".json"
            with open(path, "w") as outfile:
                json.dump(timeline, outfile)
        except URLError as e:
            if hasattr(e, "reason"):
                print("We failed to reach a server.")
                print("Reason: ", e.reason)
            elif hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: ", e.code)
