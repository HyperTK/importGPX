import os
import csv
from datetime import datetime
# pip install Pillow
from PIL import Image
import PIL.ExifTags as ExifTags


class Exif:
    '''
        Exifからgps情報を取得する
    '''
    def get_gps(self, fname):
        # 画像ファイルオープン
        im = Image.open(fname)
        # EXIF情報を取得
        exif = {
            ExifTags.TAGS[k]: v
            for k, v, in im._getexif().items()
            if k in ExifTags.TAGS
        }
        if "GPSInfo" not in exif:
            return 0.0, 0.0
        # GPS取得
        gps_tags = exif["GPSInfo"]
        datetime_original = datetime.strptime(exif["DateTime"], "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        gps = {
            ExifTags.GPSTAGS.get(t, t): gps_tags[t]
            for t in gps_tags
        }

        # 緯度経度情報を取得
        def conv_deg(v):
            print(v)
            # 分数を度に変換
            d = float(v[0])
            m = float(v[1])
            s = float(v[2])
            return d + (m / 60.0) + (s / 3600.0)
        lat = conv_deg(gps["GPSLatitude"])
        lat_ref = gps["GPSLatitudeRef"]
        if lat_ref != "N":
            lat = 0 - lat
        lon = conv_deg(gps["GPSLongitude"])
        lon_ref = gps["GPSLongitudeRef"]
        if lon_ref != "E":
            lon = 0 - lon

        return lat, lon, datetime_original

    '''
        ディレクトリ一覧を取得する
    '''
    def get_file_list(self, path):
        li = []
        for d in os.listdir(path):
            # ディレクトリのみを対象とする
            if "." in d:
                continue
            dir = "\\".join([path, d])
            files = os.listdir(dir)
            if len(files) > 0:
                for f in files:
                    filepath = "\\".join([dir, f])
                    li.append(filepath)
        return li

    '''
        ディレクトリ内の画像からGPS情報を取得しリストで返す
    '''
    def get_gps_list(self, paths):
        li = []
        for p in paths:
            root, ext = os.path.splitext(p)
            if str.upper(ext) in [".JPG", ".PNG"]:
                lat, lon, original_time = self.get_gps(p)

                arr = root.split("\\")
                dic = {
                    "filename": arr[-1],
                    "lat": lat,
                    "lon": lon,
                    "datetime": original_time
                }
                li.append(dic)
                print(p, lat, lon, original_time)
        return li

    '''
        GPS情報をCSVに出力する
    '''
    def output_csv(self, path, files):
        filename = "gps_info.csv"
        save_path = "\\".join([path, filename])
        with open(save_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(files)
