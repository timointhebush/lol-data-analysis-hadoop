import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c


def decompose_puuid_league_entries_page(tier, division):
    puuid_league_entries_path = p.get_data_path("puuid_league_entries", tier, division)
    puuid_league_entries_page_names = os.listdir(puuid_league_entries_path)

    puuid_path = p.get_data_path("puuid", tier, division)

    for puuid_league_entries_page_name in puuid_league_entries_page_names:
        print(f"{puuid_league_entries_page_name}")
        puuid_league_entries_page_path = puuid_league_entries_path + puuid_league_entries_page_name
        puuid_league_entries_page_json = c.get_json_dict(puuid_league_entries_page_path)
        page_json_len = len(puuid_league_entries_page_json)
        for i, summoner in enumerate(puuid_league_entries_page_json):
            puuid = summoner["puuid"]
            fianl_puuid_path = puuid_path + puuid
            c.store_json(fianl_puuid_path, None)
            if (i + 1) % 10 == 0:
                percent = round(i / page_json_len * 100, 2)
                print(f"{puuid_league_entries_page_name} : {percent}%")


if __name__ == "__main__":
    tiers = ["SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    divisions = ["I", "II", "III", "IV"]
    for tier in tiers:
        for division in divisions:
            decompose_puuid_league_entries_page(tier, division)
