import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c
from tools import url
from urllib.error import URLError


def collect_additional_match_data(tier, division, headers):
    """ """
    match_ids_decomposed_path = p.get_data_path("match_ids_decomposed", tier, division)

    matches_path = p.get_data_path("matches", tier, division)
    timelines_path = p.get_data_path("timelines", tier, division)

    match_ids_list = os.listdir(match_ids_decomposed_path)
    match_id_num = len(match_ids_list)

    # match id가 클 수록 최신 게임이므로 역방향으로.

    for idx in range(match_id_num - 1, -1, -1):
        match_id = match_ids_list[idx]
        if match_id[:2] != "KR":
            continue
        match_json_name = p.match_json_name(match_id)
        match_json_path = matches_path + match_json_name
        timeline_json_name = p.timeline_json_name(match_id)
        timeline_json_path = timelines_path + timeline_json_name

        if not os.path.exists(match_json_path):
            try:
                MATCH_URL = url.match_url(match_id)
                match = c.request_api(MATCH_URL, headers)
                print(f"{match_id} match 요청")
                c.store_json(match_json_path, match)
                print(match_json_path + " 저장")

                TIMELINE_URL = url.timeline_url(match_id)
                timeline = c.request_api(TIMELINE_URL, headers)
                print(f"{match_id} tiemline 요청")
                c.store_json(timeline_json_path, timeline)
                print(timeline_json_path + " 저장")
            except URLError as e:
                if hasattr(e, "reason"):
                    print("We failed to reach a server.")
                    print("Reason: ", e.reason)
                    print(f"api limit보다 많은 요청 으로 인해 10초 대기")
                    time.sleep(12)
                elif hasattr(e, "code"):
                    print("The server couldn't fulfill the request.")
                    print("Error code: ", e.code)
        else:
            print("{match_id}: 이미 존재하는 match")
