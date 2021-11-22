def league_entries_url(tier, division, page_num):
    url = f"https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page_num}"
    return url


def puuid_league_entries_url(summoner_id):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    return url


def match_ids_url(puuid):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100"
    return url


def match_url(match_id):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}"
    return url


def timeline_url(match_id):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    return url
