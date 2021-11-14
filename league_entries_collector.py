# -*- coding: utf-8 -*-

from urllib.error import URLError
import path as p
import collector as c
import url, time


def collect_league_entries(tier, headers):
    """Riot에서 제공하는 API를 이용하여 특정 tier의 사용자 정보가 담긴 page들을 json파일로 저장합니다.

    Args:
        tier: ["SILVER", "GOLD", "PLATINUM", "DIAMOND"] 중 하나로서, 사용자의 tier를 의미
        headers: API호출에 필요한 headers

    """
    divisions = ["II", "III", "IV", "I"]
    for division in divisions:
        league_entries_path = p.get_data_path("league_entries", tier, division)
        p.check_path(league_entries_path)
        page_num = 1
        while True:
            try:
                URL = url.league_entries_url(tier, division, page_num)
                league_entry_json = c.request_api(URL, headers)
                if len(league_entry_json) == 0:
                    print(f"Page {page_num}에 더 이상 소환사 목록이 없습니다.")
                    break
                league_entry_json_name = p.league_entry_json_name(tier, division, page_num)
                league_entry_json_path = league_entries_path + league_entry_json_name
                c.store_json(league_entry_json_path, league_entry_json)
                page_num += 1
            except URLError as e:
                if hasattr(e, "reason"):
                    print("We failed to reach a server.")
                    print("Reason: ", e.reason)
                    print("api limit보다 많은 요청 으로 인해 10초 대기")
                    time.sleep(12)
                elif hasattr(e, "code"):
                    print("The server couldn't fulfill the request.")
                    print("Error code: ", e.code)
