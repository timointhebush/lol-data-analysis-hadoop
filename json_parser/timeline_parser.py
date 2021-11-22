import sys, os, csv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import path as p
import collector as c


def parse_timeline_json(tier, division):
    timelines_path = p.get_data_path("timelines", tier, division)
    timeline_json_file_names = os.listdir(timelines_path)
    total_json_files = len(timeline_json_file_names)
    if total_json_files == 0:
        print("no timeline data")
        return

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
    field_idx = {f: i for i, f in enumerate(fields)}

    for i, timeline_json_file_name in enumerate(timeline_json_file_names):
        try:
            timeline_json_file_path = timelines_path + timeline_json_file_name
            timeline_json_file = c.get_json_dict(timeline_json_file_path)
            match_id = timeline_json_file["metadata"]["matchId"]
            row = [None for _ in range(len(fields))]
            row[0], row[1], row[2] = tier, division, match_id

            timeline_csv_name = p.timeline_csv_name(match_id)
            timeline_csv_file_path = (
                p.get_data_path("timeline_csv", tier, division) + timeline_csv_name
            )
            if os.path.exists(timeline_csv_file_path):
                print("이미 csv파일이 존재함")
                continue

            out_file = open(timeline_csv_file_path, "w", newline="")
            write = csv.writer(out_file)
            write.writerow(fields)

            frames = timeline_json_file["info"]["frames"]
            for frame_n, frame in enumerate(frames):
                events = frame["events"]
                for event_n, event in enumerate(events):
                    for key, value in event.items():
                        if key in field_idx:
                            row[field_idx[key]] = value
                    write.writerow(row)
            out_file.close()

            if (i + 1) % 1000 == 0:
                percent = (i + 1) / total_json_files * 100
                print(f"{tier}, {division} timeline {percent}% 처리")

        except IndexError as e:
            print(e)
            print("에러 발생 생략")
    print(f"{timeline_csv_file_path} 저장")


if __name__ == "__main__":
    tiers = ["SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    divisions = ["I", "II", "III", "IV"]
    for tier in tiers:
        for division in divisions:
            parse_timeline_json(tier, division)
