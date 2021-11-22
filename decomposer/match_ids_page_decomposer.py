import path as p
import collector as c
import os


def decompose_match_ids_page(tier, division):
    match_ids_path = p.get_data_path("match_ids", tier, division)
    match_ids_page_names = os.listdir(match_ids_path)

    if len(match_ids_page_names) == 0:
        print("데이터 없음")
        return

    match_ids_decomposed_path = p.get_data_path("match_ids_decomposed", tier, division)

    for match_ids_page_name in match_ids_page_names:
        match_ids_page_path = match_ids_path + match_ids_page_name
        match_ids_page_json = c.get_json_dict(match_ids_page_path)
        print(len(match_ids_page_json))
        for i, match_id in enumerate(match_ids_page_json):
            match_id_path = match_ids_decomposed_path + match_id
            c.store_json(match_id_path, None)


if __name__ == "__main__":
    tiers = ["SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    divisions = ["I", "II", "III", "IV"]
    for tier in tiers:
        for division in divisions:
            decompose_match_ids_page(tier, division)
