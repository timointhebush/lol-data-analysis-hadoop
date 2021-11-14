from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import time


def request_api(URL, headers):
    req = Request(URL, headers=headers)
    try:
        response = urlopen(req)
        json = json.loads(response.read().decode("utf-8"))
        print("request success")
        return json
    except URLError as e:
        if hasattr(e, "reason"):
            print("We failed to reach a server.")
            print("Reason: ", e.reason)
            print(f"api limit보다 많은 요청 으로 인해 10초 대기")
            time.sleep(12)
            raise URLError
        elif hasattr(e, "code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
    except:
        print("기타 오류가 발생했습니다.")
        pass


def json_generator(json_dict):
    for idx, data in enumerate(json_dict):
        yield idx, data


def get_json_dict(json_path):
    with open(json_path, "r") as f:
        json_file = json.load(f)
        return json_file


def store_json(json_path, data):
    with open(json_path, "w") as outfile:
        json.dump(data, outfile)
        outfile.close()
