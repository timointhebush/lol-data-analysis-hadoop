# -*- coding: utf-8 -*-
import league_entries_collector
import puuid_league_entries_collector
import match_id_collector
import match_data_collector
from tools import collector

if __name__ == "__main__":
    args = collector.define_argparser()
    headers = collector.define_headers(args.api_key)
    print(headers["X-Riot-Token"])
    # league_entries_collector.collect_league_entries(args.tier, headers)
    # puuid_league_entries_collector.collect_puuid_league_entries(args.tier, headers)
    # match_id_collector.collect_match_id(args.tier, headers)
    match_data_collector.collect_match_data(args.tier, headers)
