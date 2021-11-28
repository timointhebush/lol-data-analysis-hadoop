import sys, os, csv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c


def parse_match_json(tier, division):
    """match json파일을 csv파일로 paring하여 저장한다.
    여러 match json파일을 합쳐 하나의 csv형태가 된다.

    Args:
        tier: parsing하고자 하는 tier
        division: parsing하고자 하는 division
    """
    # match json파일들이 저장되어있는 path
    matches_path = p.get_parent_data_path("matches", tier, division)
    matches_dir_list = os.listdir(matches_path)

    # 만약 디렉토리에 폴더가 하나도 없다면, parsing할 수 없음.
    if len(matches_dir_list) == 0:
        print("no match data")
        return

    # match json 파일들이 저장된 디렉토리 중 가장 마지막 폴더 번호
    last_match_dir_num = int(sorted(matches_dir_list)[-1])

    # 하나로 저장 될 match csv 파일 이름, 경로
    match_csv_name = p.match_csv_name(tier, division, last_match_dir_num)
    match_csv_file_path = p.get_parent_data_path("match_csv", tier, division) + match_csv_name

    # csv fields
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
    # parsing에 필요한 데이터 오브젝트들.
    objectives = ["baron", "champion", "dragon", "inhibitor", "riftHerald", "tower"]

    # match csv파일 해당 경로에 생성
    out_file = open(match_csv_file_path, "w", newline="")
    write = csv.writer(out_file)
    # csv fields입력
    write.writerow(fields)

    # 마지막 수집한 match 데이터들이 담긴 경로
    match_json_path = p.get_additional_data_path("matches", tier, division, last_match_dir_num)
    # match json 파일 이름 리스트
    match_json_list = os.listdir(match_json_path)
    for i, match_json_file_name in enumerate(match_json_list):
        try:
            # csv 하나의 row를 담을 리스트
            row = []
            # 읽어드릴 match json 최종 경로
            target_match_json_path = match_json_path + match_json_file_name
            # json파일 load
            match_json_file = c.get_json_dict(target_match_json_path)
            # parsing
            teams = match_json_file["info"]["teams"]
            row.append(match_json_file["metadata"]["matchId"])
            for team in range(2):
                for obj in objectives:
                    for data_type in ["first", "kills"]:
                        row.append(teams[team]["objectives"][obj][data_type])
                row.append(teams[team]["win"])
            # parsing한 데이터를 row에 넣고, 이를 csv에 write
            write.writerow(row)
            # 진행도를 나타내는 코드
            if (i + 1) % 1000 == 0:
                percent = (i + 1) / len(match_json_list) * 100
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
            parse_match_json(tier, division)
