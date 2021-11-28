import os, random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c
from tools import url

from urllib.error import URLError


def collect_additional_match_id(tier, division, headers):
    """소환사 puuid로부터 추가적인 match_id들을 수집하기 위한 함수

    Args:
        tier: ["SILVER", "GOLD", "PLATINUM", "DIAMOND"] 중 하나로서, 사용자의 tier를 의미
        division: ["I", "II", "III", "IV"] 중 하나,
        headers: API호출에 필요한 headers
    """
    # puuid 저장 경로
    puuid_path = p.get_data_path("puuid", tier, division)
    # 기존 수집한 match id 저장 경로
    match_ids_decomposed_path = p.get_data_path("match_ids_decomposed", tier, division)
    # 마지막으로 추가 수집했을 때 저장한 폴더의 번호가 몇번인지 파악.
    last_request_num = len(os.listdir(match_ids_decomposed_path))
    # puuid 목록 리스트 생성
    puuid_list = os.listdir(puuid_path)
    # 저장 여부를 판단할 경로와,
    last_match_ids_path = p.get_additional_data_path(
        "match_ids_composed", tier, division, last_request_num
    )
    new_match_ids_path = p.get_additional_data_path(
        "match_ids_composed", tier, division, last_request_num + 1
    )
    #
    for _ in range(len(puuid_list)):
        try:
            # 요청한 match id를 담을 list
            match_ids = []
            # puuid 목록 중 임의로 하나의 puuid를 샘플링
            puuid = random.sample(puuid_list, 1)[0]
            # 해당 puuid를 통해 api request
            URL = url.match_ids_url(puuid)
            print(URL)
            match_ids = c.request_api(URL, headers)
            print(f"puuid 요청")
        except URLError as e:
            if hasattr(e, "reason"):
                print("We failed to reach a server.")
                print("Reason: ", e.reason)
                print(f"api limit보다 많은 요청 으로 인해 10초 대기")
                time.sleep(12)
            elif hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: ", e.code)

        # api request를 통해 받은 match id들 중, 이미 수집한 것들을 제거
        for match_id in match_ids:
            # 해당 match id가 존재하는지 확인하기 위한 경로
            last_match_id_path = last_match_ids_path + match_id
            # 이전 저장 경로에 존재하지 않는다면 새로운 경로에 저장.
            if not os.path.exists(last_match_id_path):
                c.store_json(new_match_ids_path + match_id, None)
                print(f"{match_id} 저장")
            else:
                print("이미 존재하는 match id")


# if __name__ == '__main__':
