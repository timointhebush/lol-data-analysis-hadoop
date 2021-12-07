import os


def get_data_path(data_type, tier, division):
    path = f"./data/{tier}/{data_type}/{division}/"
    check_path(path)
    return path


def get_parent_data_path(data_type, tier, division):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_dir = "/".join(file_dir.split("/")[:-1])
    path = f"/data/{tier}/{data_type}/{division}/"
    check_path(file_dir + path)
    return file_dir + path


def get_additional_data_path(data_type, tier, division, last_num):
    path = get_parent_data_path(data_type, tier, division)
    additional_path = path + str(last_num) + "/"
    check_path(additional_path)
    return additional_path


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


def match_csv_name(tier, division, last_num):
    name = f"match_{tier}_{division}_{last_num}.csv"
    return name


def timeline_json_name(match_id):
    name = f"timeline_{match_id}.json"
    return name


def timeline_csv_name(match_id):
    name = f"timeline_{match_id}.csv"
    return name


def check_path(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory")
