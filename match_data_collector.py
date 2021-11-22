from tools import path as p
from tools import collector as c
import os, url, time
from urllib.error import URLError


def collect_match_data(tier, headers):
    """
    Args:
        data_type: "matches" 혹은 "timelines"
    """
    divisions = ["I", "II", "III", "IV"]
    for division in divisions:
        match_ids_path = p.get_data_path("match_ids", tier, division)
        matches_path = p.get_data_path("matches", tier, division)
        timelines_path = p.get_data_path("timelines", tier, division)
        p.check_path(matches_path)
        p.check_path(timelines_path)
        file_list = os.listdir(match_ids_path)
        for page_num, match_ids_json_name in enumerate(file_list):
            match_ids_json_path = match_ids_path + match_ids_json_name
            match_ids = c.get_json_dict(match_ids_json_path)
            match_ids_generator = c.json_generator(match_ids)
            idx, match_id = next(match_ids_generator)
            while True:
                try:
                    try:
                        MATCH_URL = url.match_url(match_id)
                        match_json_name = p.match_json_name(match_id)
                        match = c.request_api(MATCH_URL, headers)
                        print(f"{page_num} + 1 페이지 {idx}번째 match")

                        match_json_path = matches_path + match_json_name
                        print(match_json_path + " 저장")
                        c.store_json(match_json_path, match)

                        TIMELINE_URL = url.timeline_url(match_id)
                        timeline_json_name = p.timeline_json_name(match_id)
                        timeline = c.request_api(TIMELINE_URL, headers)
                        print(f"{page_num} + 1 페이지 {idx}번째 tiemline")

                        timeline_json_path = timelines_path + timeline_json_name
                        print(timeline_json_path + " 저장")
                        c.store_json(timeline_json_path, timeline)
                    except URLError as e:
                        if hasattr(e, "reason"):
                            print("We failed to reach a server.")
                            print("Reason: ", e.reason)
                            print(f"api limit보다 많은 요청 으로 인해 10초 대기")
                            time.sleep(12)
                        elif hasattr(e, "code"):
                            print("The server couldn't fulfill the request.")
                            print("Error code: ", e.code)

                    idx, match_id = next(match_ids_generator)
                except StopIteration as e:
                    print("마지막")
                    break
