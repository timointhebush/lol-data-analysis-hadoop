from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import os
import time
import check_path


def collect_puuid_league_entries(tier, headers):
    """사용자 정보가 담긴 league_entries json을 읽어 사용자 puuid가 담긴 json파일을 불러옵니다.

    Args:
        tier: ["SILVER", "GOLD", "PLATINUM", "DIAMOND"] 중 하나로서, 사용자의 tier를 의미
        headers: API호출에 필요한 headers
    """
    # puuid league entries를 저장할 경로
    puuid_league_entries_path = f"./data/{tier}/puuid_league_entries"
    # league entry들이 저장되어진 경로
    league_entries_path = f"./data/{tier}/league_entries"
    # 경로에 폴더가 없다면 생성.
    check_path.check_path(puuid_league_entries_path)
    divisions = ["I", "II", "III", "IV"]
    for division in divisions:
        league_entries_division_path = league_entries_path + "/" + division
        puuid_league_entries_division_path = puuid_league_entries_path + "/" + division
        # league_entries를 저장하면서 생성한 info json파일 load
        info_json_name = f"./data/{tier}/league_entries/{division}/info/{tier}_{division}_league_entries_info.json"
        with open(info_json_name, "r") as f:
            info_json = json.load(f)
            last_page = info_json["last_page"]
            f.close()
        for page in range(1, last_page + 1):
            # 불러올 league entry json 경로
            league_entry_json_name = f"{tier}_{division}_page_{page}.json"
            league_entry_json_path = league_entries_division_path + "/" + league_entry_json_name
            # puuid가 담길 page
            page_list = []
            with open(league_entry_json_path, "r") as f:
                league_entry_json = json.load(f)
                for idx, summoner in enumerate(league_entry_json):
                    summoner_id = summoner["summonerId"]
                    PUUID_LEAGUE_ENTRIES_URL = (
                        f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
                    )
                    req = Request(PUUID_LEAGUE_ENTRIES_URL, headers=headers)
                    try:
                        response = urlopen(req)
                        puuid_summoner = json.loads(response.read().decode("utf-8"))
                        print(f"{tier}_{division}_page_{page}.json의 {idx}번째 ")
                        page_list += [puuid_summoner]
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
            puuid_league_entries_json_name = f"puuid_{tier}_{division}_page_{page}.json"
            final_path = puuid_league_entries_division_path + "/" + puuid_league_entries_json_name
            with open(final_path, "w") as outfile:
                json.dump(page, outfile)
