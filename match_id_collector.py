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
            page_list = []
            with open(puuid_league_entry_json_path, "r") as f:
                puuid_league_entry_json = json.load(f)
                for idx, summoner in enumerate(puuid_league_entry_json):
                    puuid = summoner["puuid"]
                    MATCH_ID_URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100"
                    req = Request(MATCH_ID_URL, headers=headers)
                    try:
                        response = urlopen(req)
                        match_ids = json.loads(response.read().decode("utf-8"))
                        print(f"{idx}번째 소환사의 match id를 저장")
                        page_list += match_ids
                    except URLError as e:
                        if hasattr(e, "reason"):
                            print("We failed to reach a server.")
                            print("Reason: ", e.reason)
                            print(f"{page}번의 요청 으로 인해 10초 대기")
                            time.sleep(12)
                        elif hasattr(e, "code"):
                            print("The server couldn't fulfill the request.")
                            print("Error code: ", e.code)
                    except:
                        pass
                f.close()
            page = puuid_json_name[-6]
            match_ids_json_name = f"match_ids_{tier}_{division}_page_{page}.json"
            final_path = match_ids_division_path + "/" + match_ids_json_name
            # 중복 게임 제거 후 저장
            page_list = list(set(page_list))
            with open(final_path, "w") as outfile:
                json.dump(page_list, outfile)
