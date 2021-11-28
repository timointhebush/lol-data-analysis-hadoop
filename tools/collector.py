from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse, json, time, argparse


def request_api(URL, headers):
    req = Request(URL, headers=headers)
    response = urlopen(req)
    json_file = json.loads(response.read().decode("utf-8"))
    print("request success")
    return json_file


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


def define_argparser():
    p = argparse.ArgumentParser(description="수집하고자 하는 티어와 API KEY를 입력하세요")

    p.add_argument("--tier", required=True)
    p.add_argument("--api_key", required=True)

    args = p.parse_args()
    return args


def define_headers(api_key):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30",
        "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": "",
    }
    headers["X-Riot-Token"] = api_key
    return headers
