import sys, os, csv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c


def parse_timeline_json(tier, division):
    """timeline json파일을 csv파일로 paring하여 저장한다.

    Args:
        tier: parsing하고자 하는 tier
        division: parsing하고자 하는 division
    """
    # parsing해야하는 timeline json들이 저장되어 있는 경로
    timelines_path = p.get_parent_data_path("timelines", tier, division)
    print(timelines_path)
    timelines_dir_list = os.listdir(timelines_path)
    print(timelines_dir_list)

    # 디렉토리에 폴더가 없다면 parsing 불가
    if len(timelines_dir_list) == 0:
        print("no timeline data")
        return

    # timeline json들이 저장된 디렉토리 중 가장 마지막 폴더 번호
    last_timeline_dir_num = int(sorted(timelines_dir_list)[-1])

    # timeline csv저장될 경로.
    timeline_csv_path = p.get_additional_data_path(
        "timeline_csv", tier, division, last_timeline_dir_num
    )

    # csv fields
    fields = [
        "tier",
        "division",
        "match_id",
        "timestamp",
        "type",
        "winningTeam",
        "afterId",
        "ascendedType",
        "beforeId",
        "buildingType",
        "creatorId",
        "eventType",
        "framesInterval",
        "itemId",
        "killerId",
        "laneType",
        "levelUpType",
        "monsterSubType",
        "monsterType",
        "participantId",
        "pointCaptured",
        "skillSlot",
        "teamId",
        "towerType",
        "victimId",
        "wardType",
    ]
    # csv중 특정 column에 값을 넣기 위한 dix dictionary
    field_idx = {f: i for i, f in enumerate(fields)}

    # 마지막 수집한 timeline 데이터들이 담긴 디렉토리 경로, json 리스트
    timeline_json_path = p.get_additional_data_path(
        "timelines", tier, division, last_timeline_dir_num
    )
    timeline_json_list = os.listdir(timeline_json_path)
    for i, timeline_json_file_name in enumerate(timeline_json_list):
        try:
            # 로드할 timeline json 경로와, 파일
            timeline_json_file_path = timeline_json_path + timeline_json_file_name
            timeline_json_file = c.get_json_dict(timeline_json_file_path)

            # parsing 기본사항들
            match_id = timeline_json_file["metadata"]["matchId"]
            row = [None for _ in range(len(fields))]
            row[0], row[1], row[2] = tier, division, match_id

            # timeline csv 경로 설정.
            timeline_csv_name = p.timeline_csv_name(match_id)
            final_timeline_csv_path = timeline_csv_path + timeline_csv_name

            if os.path.exists(final_timeline_csv_path):
                print("이미 csv파일이 존재함")
                continue

            # csv 파일 생성 및 field 입력
            out_file = open(final_timeline_csv_path, "w", newline="")
            write = csv.writer(out_file)
            write.writerow(fields)

            # parsing, csv write
            frames = timeline_json_file["info"]["frames"]
            for frame_n, frame in enumerate(frames):
                events = frame["events"]
                for event_n, event in enumerate(events):
                    for key, value in event.items():
                        if key in field_idx:
                            row[field_idx[key]] = value
                    write.writerow(row)
            out_file.close()

            # 진행도
            if (i + 1) % 1000 == 0:
                percent = (i + 1) / len(timeline_json_list) * 100
                print(f"{tier}, {division} timeline {percent}% 처리")

        except IndexError as e:
            print(e)
            print("에러 발생 생략")
    print(f"{final_timeline_csv_path} 저장")


if __name__ == "__main__":
    tiers = ["SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    divisions = ["I", "II", "III", "IV"]
    for tier in tiers:
        for division in divisions:
            parse_timeline_json(tier, division)
