import path as p
import collector as c
import os, url, time
from urllib.error import URLError


def collect_match_data(tier, headers, data_type):
    """
    Args:
        data_type: "matches" 혹은 "timelines"
    """
    divisions = ["I", "II", "III", "IV"]
    for division in divisions:
        match_ids_path = p.get_data_path("match_ids", tier, division)
        data_path = p.get_data_path(data_type, tier, division)
        p.check_path(data_path)
        file_list = os.listdir(match_ids_path)
        for page_num, match_ids_json_name in enumerate(file_list):
            match_ids_json_path = match_ids_path + match_ids_json_name
            match_ids = c.get_json_dict(match_ids_json_path)
            match_ids_generator = c.json_generator(match_ids)
            idx, match_id = next(match_ids_generator)
            while True:
                try:
                    if data_type == "matches":
                        URL = url.match_url(match_id)
                        data_json_name = p.match_json_name(match_id)
                    else:  # timelines
                        URL = url.timeline_url(match_id)
                        data_json_name = p.timeline_json_name(match_id)
                    data = c.request_api(URL, headers)
                    print(f"{page_num} + 1 페이지 {idx}번째 {data_type}")
                    # match data 수정
                    data_json_path = data_path + data_json_name
                    print(data_json_name + " 저장")
                    c.store_json(data_json_path, data)
                    idx, match_id = next(match_ids_generator)
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
