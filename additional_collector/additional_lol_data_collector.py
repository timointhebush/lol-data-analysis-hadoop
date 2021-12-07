import additional_match_id_collector as ai
import additional_match_data_collector as ad
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tools import collector as c


if __name__ == "__main__":
    args = c.define_argparser()
    headers = c.define_headers(args.api_key)
    print(headers["X-Riot-Token"])
    tiers = ["SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    divisions = ["I", "II", "III", "IV"]
    for tier in tiers:
        for division in divisions:
            ai.collect_additional_match_id(tier, division, headers)
            ad.collect_additional_match_data(tier, division, headers)
