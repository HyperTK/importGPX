import csv
import copy
from gpx import Gpx
from exif import Exif


'''
    GPS情報をCSVに出力する
'''


def output_csv(path, files, fieldnames):
    filename = "gps_info.csv"
    save_path = "\\".join([path, filename])
    with open(save_path, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(files)


'''
    GPSの辞書と写真のExifの辞書を比較する
'''


def comp_dict(gps_dict, photo_dict):
    li = []
    for photo in photo_dict:
        newTarget = []
        t = photo["datetime"]
        name = photo["filename"]
        if name == "IMG_7022":
            print(name)

        target = list(filter(lambda item: item["datetime"] == t, gps_dict))
        newTarget = copy.deepcopy(target)
        for i in newTarget:
            i["name"] = name

        print(newTarget)

        if len(newTarget) > 0:
            li.extend(newTarget)
    return li


if __name__ == "__main__":
    gpx = Gpx()
    exif = Exif()
    # GPXをパースして座標と時間の組み合わせを取得する
    gpx_dict = gpx.get_gps_data("input\\gpx\\input.gpx")
    # 写真からGPSを取得する
    files = exif.get_file_list("input")
    photo_gps_dict = exif.get_gps_list(files)
    # 辞書を比較して一致するデータを取得する
    gps_list = comp_dict(gpx_dict, photo_gps_dict)
    # CSVに出力する
    field_name = ["name", "lat", "lng", "datetime", "datetime_second"]
    output_csv("result\\", gps_list, field_name)
    print("出力完了")
