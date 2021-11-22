import os, random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools import path as p
from tools import collector as c
from tools import url

from urllib.error import URLError


def collect_additional_match_id(tier, division, headers):
    """ """
    puuid_path = p.get_data_path("puuid", tier, division)
    match_ids_decomposed_path = p.get_data_path("match_ids_decomposed", tier, division)
    puuid_list = os.listdir(puuid_path)

    for _ in range(len(puuid_list)):
        try:
            match_ids = []
            puuid = random.sample(puuid_list, 1)[0]
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

        for match_id in match_ids:
            match_id_path = match_ids_decomposed_path + match_id
            if not os.path.exists(match_id_path):
                c.store_json(match_id_path, None)
                print(f"{match_id} 저장")
            else:
                print("이미 존재하는 match id")


# if __name__ == '__main__':
