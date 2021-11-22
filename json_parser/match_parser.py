import sys, os, csv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import path as p
import collector as c


def parse_match_json(tier, division, ver):
    matches_path = p.get_data_path("matches", tier, division)
    match_json_file_names = os.listdir(matches_path)
    total_json_files = len(match_json_file_names)
    if total_json_files == 0:
        print("no match data")
        return

    match_csv_name = p.match_csv_name(tier, division, ver)
    match_csv_file_path = p.get_data_path("match_csv", tier, division) + match_csv_name
    if os.path.exists(match_csv_file_path):
        print("이미 csv파일이 존재함")
        return

    fields = [
        "match_id",
        "0_baron_first",
        "0_baron_kills",
        "0_champion_first",
        "0_champion_kills",
        "0_dragon_first",
        "0_dragon_kills",
        "0_inhibitor_first",
        "0_inhibitor_kills",
        "0_riftHerald_first",
        "0_riftHerald_kills",
        "0_tower_first",
        "0_tower_kills",
        "0_win",
        "1_baron_first",
        "1_baron_kills",
        "1_champion_first",
        "1_champion_kills",
        "1_dragon_first",
        "1_dragon_kills",
        "1_inhibitor_first",
        "1_inhibitor_kills",
        "1_riftHerald_first",
        "1_riftHerald_kills",
        "1_tower_first",
        "1_tower_kills",
        "1_win",
    ]
    objectives = ["baron", "champion", "dragon", "inhibitor", "riftHerald", "tower"]

    out_file = open(match_csv_file_path, "w", newline="")
    write = csv.writer(out_file)
    write.writerow(fields)
    for i, match_json_file_name in enumerate(match_json_file_names):
        try:
            row = []
            match_json_file_path = matches_path + match_json_file_name
            match_json_file = c.get_json_dict(match_json_file_path)
            teams = match_json_file["info"]["teams"]
            row.append(match_json_file["metadata"]["matchId"])
            for team in range(2):
                for obj in objectives:
                    for data_type in ["first", "kills"]:
                        row.append(teams[team]["objectives"][obj][data_type])
                row.append(teams[team]["win"])
            write.writerow(row)
            if (i + 1) % 1000 == 0:
                percent = (i + 1) / total_json_files * 100
                print(f"{tier}, {division}, ver: {ver} match {percent}% 처리")
        except IndexError as e:
            print(e)
            print("에러 발생 생략")
    print(f"{match_csv_file_path} 저장")


if __name__ == "__main__":
    tiers = ["SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    divisions = ["I", "II", "III", "IV"]
    for tier in tiers:
        for division in divisions:
            parse_match_json(tier, division, 1)
