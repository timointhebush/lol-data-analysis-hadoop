import argparse
import league_entries_collecter


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


if __name__ == "__main__":
    args = define_argparser()
    headers = define_headers(args.api_key)
    print(headers["X-Riot-Token"])
    league_entries_collecter.collect_league_entries(args.tier, headers)
