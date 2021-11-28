import os, random, sys, time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c
from tools import url

from urllib.error import URLError


def collect_additional_match_data(tier, division, headers):
    """match id로부터 추가적인 match, timeline 데이터들을 수집하기 위한 함수

    Args:
        tier: ["SILVER", "GOLD", "PLATINUM", "DIAMOND"] 중 하나로서, 사용자의 tier를 의미
        division: ["I", "II", "III", "IV"] 중 하나,
        headers: API호출에 필요한 headers
    """
    # match ids가 저장된 경로
    match_ids_decomposed_path = p.get_parent_data_path("match_ids_decomposed", tier, division)

    # 마지막 저장한 match id 디렉토리 경로
    match_ids_dir_list = os.listdir(match_ids_decomposed_path)
    # 마지막 저장한 match id 디렉토리 번호
    last_match_ids_num = int(sorted(match_ids_dir_list)[-1])

    # 지난 match와 timeline데이터들이 저장된 경로.
    last_matches_path = p.get_additional_data_path("matches", tier, division, last_match_ids_num)
    last_timelines_path = p.get_additional_data_path(
        "timelines", tier, division, last_match_ids_num
    )

    # match와 timeline데이터들이 저장될 경로.
    matches_path = p.get_additional_data_path("matches", tier, division, last_match_ids_num + 1)
    timelines_path = p.get_additional_data_path("timelines", tier, division, last_match_ids_num + 1)

    # 데이터를 불러올 match id가 저장된 경로
    target_match_ids_path = p.get_additional_data_path(
        "match_ids_decomposed", tier, division, last_match_ids_num
    )
    # 데이터를 불러올 match id리스트
    target_match_ids_list = os.listdir(target_match_ids_path)

    # match id가 클 수록 최신 게임이므로 역방향으로.
    for idx in range(len(target_match_ids_list) - 1, -1, -1):
        match_id = target_match_ids_list[idx]
        # match_id가 아닌 것들을 걸러내기위한 장치
        if match_id[:2] != "KR":
            continue
        # match 데이터
        match_json_name = p.match_json_name(match_id)
        match_json_path = matches_path + match_json_name
        # 기존에 저장된 데이터인지 확인하기 위한 경로
        last_match_json_path = last_matches_path + match_json_name
        # timeline 데이터
        timeline_json_name = p.timeline_json_name(match_id)
        timeline_json_path = timelines_path + timeline_json_name

        if not os.path.exists(last_match_json_path):
            try:
                # match 데이터 저장
                MATCH_URL = url.match_url(match_id)
                match = c.request_api(MATCH_URL, headers)
                print(f"{match_id} match 요청")
                c.store_json(match_json_path, match)
                print(match_json_path + " 저장")
                # timeline 데이터 저장
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


if __name__ == "__main__":
    args = c.define_argparser()
    headers = c.define_headers(args.api_key)
    collect_additional_match_data(args.tier, "I", headers)
