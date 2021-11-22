# -*- coding: utf-8 -*-

from urllib.error import URLError
import url, time, os
from tools import path as p
from tools import collector as c


def collect_puuid_league_entries(tier, headers):
    """사용자 정보가 담긴 league_entries json을 읽어 사용자 puuid가 담긴 json파일을 불러옵니다.

    Args:
        tier: ["SILVER", "GOLD", "PLATINUM", "DIAMOND"] 중 하나로서, 사용자의 tier를 의미
        headers: API호출에 필요한 headers
    """
    divisions = ["I", "II", "III", "IV"]
    for division in divisions:
        league_entries_path = p.get_data_path("league_entries", tier, division)
        puuid_league_entries_path = p.get_data_path("puuid_league_entries", tier, division)
        p.check_path(puuid_league_entries_path)
        file_list = os.listdir(league_entries_path)
        for page_num, league_entry_json_name in enumerate(file_list):
            league_entry_json_path = league_entries_path + league_entry_json_name
            print(league_entry_json_path)
            league_entry = c.get_json_dict(league_entry_json_path)
            league_entry_generator = c.json_generator(league_entry)
            puuid_page = []
            idx, summoner = next(league_entry_generator)
            while True:
                try:
                    summoner_id = summoner["summonerId"]
                    URL = url.puuid_league_entries_url(summoner_id)
                    puuid_summoner = c.request_api(URL, headers)
                    print(f"{page_num} + 1 페이지의 {idx}번째 summoner")
                    puuid_page += [puuid_summoner]
                    idx, summoner = next(league_entry_generator)
                except StopIteration as e:
                    print("마지막")
                    break
                except URLError as e:
                    if hasattr(e, "reason"):
                        print("We failed to reach a server.")
                        print("Reason: ", e.reason)
                        print(f"api limit보다 많은 요청 으로 인해 10초 대기")
                        time.sleep(12)
                    elif hasattr(e, "code"):
                        print("The server couldn't fulfill the request.")
                        print("Error code: ", e.code)
            puuid_league_entry_json_name = p.puuid_league_entry_json_name(
                tier, division, page_num + 1
            )
            puuid_league_entry_json_path = puuid_league_entries_path + puuid_league_entry_json_name
            print(puuid_league_entry_json_name + " 저장")
            c.store_json(puuid_league_entry_json_path, puuid_page)
