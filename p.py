import check_path

check_path.check_path("./dd")

import json

a = 3
info = {"ddd": a - 1}
with open("./dd/ss.json", "w") as outfile:
    json.dump(info, outfile)
