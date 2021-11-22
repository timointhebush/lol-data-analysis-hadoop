from urllib.error import URLError
import json, os, time, url
from tools import path as p
from tools import collector as c


def collect_match_id(tier, headers):
    """ """
    divisions = ["I", "II", "III", "IV"]
    for division in divisions:
        puuid_league_entries_path = p.get_data_path("puuid_league_entries", tier, division)
        match_ids_path = p.get_data_path("match_ids", tier, division)
        p.check_path(match_ids_path)
        file_list = os.listdir(puuid_league_entries_path)
        for page_num, puuid_league_entry_json_name in enumerate(file_list):
            puuid_league_entry_json_path = puuid_league_entries_path + puuid_league_entry_json_name
            puuid_league_entry = c.get_json_dict(puuid_league_entry_json_path)
            puuid_league_entry_generator = c.json_generator(puuid_league_entry)
            match_id_page = []
            idx, summoner = next(puuid_league_entry_generator)
            while True:
                try:
                    puuid = summoner["puuid"]
                    URL = url.match_ids_url(puuid)
                    match_ids = c.request_api(URL, headers)
                    print(f"{page_num} + 1 페이지 {idx}번째 summoner의 match id들")
                    match_id_page += match_ids
                    idx, summoner = next(puuid_league_entry_generator)
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
            match_ids_json_name = p.match_ids_json_name(tier, division, page_num + 1)
            match_ids_json_path = match_ids_path + match_ids_json_name
            print(match_ids_json_path + " 저장")
            c.store_json(match_ids_json_path, match_id_page)
