from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import check_path
import time


def collect_league_entries(tier, headers):
    """Riot에서 제공하는 API를 이용하여 특정 tier의 사용자 정보가 담긴 page들을 json파일로 저장합니다.

    Args:
        tier: ["SILVER", "GOLD", "PLATINUM", "DIAMOND"] 중 하나로서, 사용자의 tier를 의미
        headers: API호출에 필요한 headers

    """
    league_entries_path = f"./data/{tier}/league_entries"
    check_path.check_path(league_entries_path)
    divisions = ["I", "II", "III", "IV"]
    # Response가 빈 리스트가 나올 때 까지 page 증가
    for division in divisions:
        page = 1
        while True:
            LEAGUE_ENTRIES_URL = f"https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}"
            req = Request(LEAGUE_ENTRIES_URL, headers=headers)
            try:
                response = urlopen(req)
                league_entries_page = json.loads(response.read().decode("utf-8"))
                if len(league_entries_page) == 0:
                    print(f"Page {page}에 더 이상 소환사 목록이 없습니다.")
                    info = {"last_page": page - 1}
                    info_json_name = f"/info/{tier}_{division}_league_entries_info.json"
                    final_path = league_entries_path + info_json_name
                    with open(final_path, "w") as outfile:
                        json.dump(info, outfile)
                        break
                json_name = f"/{tier}_{division}_page_{page}.json"
                final_path = league_entries_path + json_name
                with open(final_path, "w") as outfile:
                    json.dump(league_entries_page, outfile)
                print(f"{tier}_{division}_page_{page}.json 저장!")
                page += 1
            except URLError as e:
                if hasattr(e, "reason"):
                    print("We failed to reach a server.")
                    print("Reason: ", e.reason)
                    print(f"{page}번의 요청 으로 인해 10초 대기")
                    time.sleep(12)
                elif hasattr(e, "code"):
                    print("The server couldn't fulfill the request.")
                    print("Error code: ", e.code)
