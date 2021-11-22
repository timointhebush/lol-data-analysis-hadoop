from lol_data_collector import *
import additional_match_id_collector
import additional_match_data_collector

if __name__ == "__main__":
    args = define_argparser()
    headers = define_headers(args.api_key)
    print(headers["X-Riot-Token"])
    # additional_match_id_collector.collect_additional_match_id("SILVER", "I", headers)
    additional_match_data_collector.collect_additional_match_data("SILVER", "I", headers)
