def get_data_path(data_type, tier, division):
    path = "./data/{tier}/{data_type}/{division}/"
    return path


def league_entry_json_name(tier, division, page_num):
    name = f"{tier}_{division}_page_{page_num}.json"
    return name


def puuid_league_entry_json_name(tier, division, page_num):
    name = f"puuid_{tier}_{division}_page_{page_num}.json"
    return name


def match_ids_json_name(tier, division, page_num):
    name = f"match_ids_{tier}_{division}_page_{page_num}.json"
    return name


def match_json_name(match_id):
    name = f"match_{match_id}.json"
    return name


def timeline_json_name(match_id):
    name = f"timeline_{match_id}.json"
    return name