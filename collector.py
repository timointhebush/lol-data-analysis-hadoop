from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json
import time


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
