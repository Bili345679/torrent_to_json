import sys
import os
import torrent_reader as tr
import common

prog_dir_name = os.path.dirname(sys.argv[0])
if len(sys.argv) < 2:
    os.system("pause")
    exit()

file_paths = sys.argv[1:]
for each in file_paths:
    if os.path.splitext(each)[1] == ".torrent" and os.path.isfile(each):
        torrent_info = tr.read_file(each)
        if "name.utf-8" in torrent_info["info"]:
            name = torrent_info["info"]["name.utf-8"]
        else:
            name = torrent_info["info"]["name"]
        json_path = f"{prog_dir_name}\\torrent_json\\{name}.json"

        real_file_path = common.json_dump(
            torrent_info,
            json_path,
            "utf8",
            True,
            ensure_ascii=False,
        )
        print(real_file_path)

os.system("pause")
