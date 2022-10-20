import gpxpy
import gpxpy.gpx
from pytz import timezone

# タイムゾーン
dt_tz = timezone('Asia/Tokyo')
# 日時文字列形式
dt_fmt1 = '%Y-%m-%d %H:%M'
dt_fmt2 = '%Y-%m-%d %H:%M:%S'
# 配列の初期化
DateTime = []
Lat = []
Lng = []
gpx_dicts = []


class Gpx:

    def get_gps_data(self, file_path):
        # GPXファイルの読み込み
        gpx_file_r = open(file_path, 'r', encoding="utf-8")
        # GPXファイルのパース
        gpx = gpxpy.parse(gpx_file_r)
        # GPXデータの読み込み
        for track in gpx.tracks:
            for segment in track.segments:
                # ポイントデータリストの読み込み
                points = segment.points
                # ポイントデータの長さ
                N = len(points)
                # ポイントデータの読み込み
                for i in range(N):
                    # ポイントデータ
                    point = points[i]
                    # データ抽出
                    datetime1 = point.time.astimezone(dt_tz).strftime(dt_fmt1)
                    datetime2 = point.time.astimezone(dt_tz).strftime(dt_fmt2)

                    lat = point.latitude
                    lng = point.longitude
                    dic = {
                        "lat": lat,
                        "lng": lng,
                        "datetime": datetime1,
                        "datetime_second": datetime2
                    }
                    gpx_dicts.append(dic)
        return gpx_dicts