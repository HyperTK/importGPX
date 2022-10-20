from gpx import Gpx
from exif import Exif


def comp_dict(gps_dict, photo_dict):
    li = []
    for photo in photo_dict:
        t = photo["datetime"]
        target = list(filter(lambda item: item["datetime"] == t, gps_dict))
        print(target)
        if len(target) > 0:
            li.extend(target)
    return li


if __name__ == "__main__":
    gpx = Gpx()
    exif = Exif()
    # GPXをパースして座標と時間の組み合わせを取得する
    gpx_dict = gpx.get_gps_data("input\\gpx\\input.gpx")
    # 写真からGPSを取得する
    files = exif.get_file_list("input")
    photo_gps_dict = exif.get_gps_list(files)
    comp_dict(gpx_dict, photo_gps_dict)
