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
    # league entry들을 저장할 경로
    league_entries_path = f"./data/{tier}/league_entries"
    # 경로에 폴더가 없다면 생성
    check_path.check_path(league_entries_path)
    divisions = ["II", "III", "IV", "I"]
    for division in divisions:
        page = 1
        while True:  # Response가 빈 리스트가 나올 때 까지 page 증가
            LEAGUE_ENTRIES_URL = f"https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}"
            req = Request(LEAGUE_ENTRIES_URL, headers=headers)
            # division별로 데이터를 저장하기 위한 경로 변수 설정 및 폴더 생성
            league_entries_division_path = league_entries_path + "/" + division
            check_path.check_path(league_entries_division_path)
            try:
                response = urlopen(req)
                league_entries_page = json.loads(response.read().decode("utf-8"))
                if len(league_entries_page) == 0:  # 불러온 page에 더이상 소환사들의 정보가 없을 경우.
                    print(f"Page {page}에 더 이상 소환사 목록이 없습니다.")
                    # 해당 division에 몇 페이지까지 존재하였는지 기록하는 json 생성.
                    info_path = league_entries_division_path + "/info"
                    check_path.check_path(info_path)
                    # 생성할 json을 위한 dictionary
                    info = {"last_page": page - 1}
                    info_json_name = f"/{tier}_{division}_league_entries_info.json"
                    final_path = info_path + info_json_name
                    # json 저장
                    with open(final_path, "w") as outfile:
                        json.dump(info, outfile)
                        break
                # 불러온 page에 소환사들 정보가 있을 경우.
                json_name = f"/{division}/{tier}_{division}_page_{page}.json"
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
            except:
                pass
