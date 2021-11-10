from urllib.request import Request, urlopen
from urllib.error import URLError
import urllib.parse
import json

LEAGUE_ENTRIES_URL = (
    "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/SILVER/I?page=1"
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30",
    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "",
}
req = Request(LEAGUE_ENTRIES_URL, headers=headers)
try:
    response = urlopen(req)
    entries_page = json.loads(response.read().decode("utf-8"))
    print(type(entries_page))
    print(entries_page[0]["wins"])
    with open("./sample.json", "w") as outfile:
        json.dump(entries_page, outfile)
except URLError as e:
    if hasattr(e, "reason"):
        print("We failed to reach a server.")
        print("Reason: ", e.reason)
    elif hasattr(e, "code"):
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
