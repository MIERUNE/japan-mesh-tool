import os
import math
import json

# メッシュコード生成範囲
MINIMUM_LON = 122.00
MAXIMUM_LON = 154.00
MINIMUM_LAT = 20.00
MAXIMUM_LAT = 46.00

# 1~7次の経緯度でのメッシュサイズ:(x, y)
MESH_SIZES = [
    (1, 2/3),
    (1/8, 1/12),
    (1/80, 1/120),
    (1/160, 1/240),
    (1/320, 1/480),
    (1/640, 1/960),
    (1/1600, 1/2400)
]


def get_start_offset(meshnum: int, lonlat: list) -> tuple:
    """[summary]
    メッシュ次数と経緯度に対し、原点（左下）から数えて何個のメッシュをスキップするか計算
    Args:
        meshnum (int): メッシュ次数
        lonlat ([float, float]): [経度, 緯度]

    Returns:
        tuple: (x方向のオフセット、y方向のオフセット)
    """
    x_mesh_dist, y_mesh_dist = MESH_SIZES[meshnum - 1]

    x_offset = 0
    while lonlat[0] >= MINIMUM_LON + x_mesh_dist * (x_offset + 1):
        x_offset += 1

    y_offset = 0
    while lonlat[1] >= MINIMUM_LAT + y_mesh_dist * (y_offset + 1):
        y_offset += 1

    return x_offset, y_offset


def get_end_offset(meshnum: int, lonlat: list) -> tuple:
    """[summary]
    メッシュ次数と経緯度に対し、終点（右上）から数えて何個のメッシュをスキップするか計算
    Args:
        meshnum (int): メッシュ次数
        lonlat ([float, float]): [経度, 緯度]

    Returns:
        tuple: (x方向のオフセット、y方向のオフセット)
    """
    x_mesh_dist, y_mesh_dist = MESH_SIZES[meshnum - 1]

    x_offset = 0
    while lonlat[0] <= MAXIMUM_LON - x_mesh_dist * (x_offset + 1):
        x_offset += 1

    y_offset = 0
    while lonlat[1] <= MAXIMUM_LAT - y_mesh_dist * (y_offset + 1):
        y_offset += 1

    return x_offset, y_offset


def get_meshes(meshnum: int, extent=None) -> list:
    """[summary]
    メッシュ次数および領域から、その領域に重なる全てのメッシュの頂点の経緯度のリストを返す

    Args:
        meshnum (int): メッシュ次数
        extent (list, optional):  経緯度のペアのリストで領域指定

    Returns:
        list: [ {"geometry":<メッシュのジオメトリ>, "code":<メッシュコード>}... ]
    """

    # メッシュのx方向y方向それぞれの数
    x_size, y_size = MESH_SIZES[meshnum - 1]
    x_mesh_count = math.ceil((MAXIMUM_LON - MINIMUM_LON) / x_size)
    y_mesh_count = math.ceil((MAXIMUM_LAT - MINIMUM_LAT) / y_size)

    # スキップすべきメッシュの数＝オフセットを計算
    start_offset = [0, 0]
    end_offset = [0, 0]
    if extent:
        min_lon = min(extent[0][0], extent[1][0])
        min_lat = min(extent[0][1], extent[1][1])
        max_lon = max(extent[0][0], extent[1][0])
        max_lat = max(extent[0][1], extent[1][1])

        # [左下経緯度, 右上経緯度]にソート
        cleaned_extent = [
            [min_lon, min_lat],
            [max_lon, max_lat]
        ]

        start_offset = get_start_offset(meshnum, cleaned_extent[0])
        end_offset = get_end_offset(meshnum, cleaned_extent[1])

    meshes = []
    for y in range(start_offset[1], y_mesh_count - end_offset[1]):
        for x in range(start_offset[0], x_mesh_count - end_offset[0]):
            mesh = get_mesh(meshnum, x, y)
            meshes.append(mesh)
    return meshes


def get_mesh(meshnum: int, x: int, y: int) -> dict:
    """[summary]
    メッシュ次数、メッシュ番地からメッシュのジオメトリとメッシュコードを返す

    Args:
        meshnum (int): メッシュ次数
        x (int): 原点から右方向に数えたメッシュ番地
        y (int): 原点から上方向に数えたメッシュ番地

    Returns:
        dict: {"geometry":<メッシュのジオメトリ>, "code":<メッシュコード>}
    """
    x_size, y_size = MESH_SIZES[meshnum - 1]
    left_lon = MINIMUM_LON + x * x_size
    bottom_lat = MINIMUM_LAT + y * y_size
    right_lon = MINIMUM_LON + (x + 1) * x_size
    top_lat = MINIMUM_LAT + (y + 1) * y_size

    code = ""
    # 緯度を1.5倍した整数値
    code += str(int(bottom_lat * 1.5))
    # 経度の整数部分の下2桁
    code += str(int(left_lon))[1:]
    # 以下、メッシュ次数に応じてコードを2桁ずつ付加
    if meshnum == 1:
        pass
    elif meshnum == 2:
        code += str(y % 8)
        code += str(x % 8)
    elif meshnum == 3:
        code += str(int((y % 80) / 10))
        code += str(int((x % 80) / 10))
        code += str(y % 10)
        code += str(x % 10)
    elif meshnum == 4:
        code += str(int((y % 160) / 20))
        code += str(int((x % 160) / 20))
        code += str(int((y % 20) / 2))
        code += str(int((x % 20) / 2))
        code += str(y % 2)
        code += str(x % 2)
    elif meshnum == 5:
        code += str(int((y % 320) / 40))
        code += str(int((x % 320) / 40))
        code += str(int((y % 40) / 4))
        code += str(int((x % 40) / 4))
        code += str(int((y % 4) / 2))
        code += str(int((x % 4) / 2))
        code += str(y % 2)
        code += str(x % 2)
    elif meshnum == 6:
        code += str(int((y % 640) / 80))
        code += str(int((x % 640) / 80))
        code += str(int((y % 80) / 8))
        code += str(int((x % 80) / 8))
        code += str(int((y % 8) / 4))
        code += str(int((x % 8) / 4))
        code += str(int((y % 4) / 2))
        code += str(int((x % 4) / 2))
        code += str(y % 2)
        code += str(x % 2)
    elif meshnum == 7:
        code += str(int((y % 1600) / 200))
        code += str(int((x % 1600) / 200))
        code += str(int((y % 200) / 20))
        code += str(int((x % 200) / 20))
        code += str(int((y % 20) / 10))
        code += str(int((x % 20) / 10))
        code += str(int((y % 10) / 5))
        code += str(int((x % 10) / 5))
        code += str(y % 5)
        code += str(x % 5)

    return {
        "geometry": [[
            [left_lon, bottom_lat],
            [left_lon, top_lat],
            [right_lon, top_lat],
            [right_lon, bottom_lat],
            [left_lon, bottom_lat]
        ]],
        "code": code
    }


if __name__ == "__main__":
    import argschems

    print("initializing...")
    # コマンド初期化
    args = argschems.ARGSCHEME.parse_args()

    # メッシュ番号
    try:
        meshnum = int(args.meshnum)
    except ValueError:
        raise ValueError(
            "メッシュ次数を正しく入力してください あなたの入力：" + str(args.meshnum))

    # 別称での指定を次数に置き換え
    if meshnum == 500:
        meshnum = 4
    elif meshnum == 250:
        meshnum = 5
    elif meshnum == 125:
        meshnum = 6
    elif meshnum == 50:
        meshnum = 7

    if meshnum < 1 or 7 < meshnum:
        raise ValueError("メッシュ次数を正しく入力してください あなたの入力：" + str(args.meshnum))

    extent_texts = args.extent
    target_dir = args.target_dir

    # 保存先未指定なら実行ディレクトリに保存
    if target_dir is None:
        target_dir = ''

    # 領域が指定されているならパース
    extent = None
    if extent_texts:
        try:
            extent = [list(map(float, extent_texts[0].split(","))),
                      list(map(float, extent_texts[1].split(",")))]
        except ValueError:
            raise ValueError(
                "領域指定が不正です：カンマ区切りの経緯度を、スペース区切りで2つ入力してください")

        # 経緯度をバリデーション
        for latlon in extent:
            for value in latlon:
                if not -180 < value < 180:
                    raise ValueError("経緯度は-180から180の間で指定してください")

    print("making meshes...")
    # メッシュ生成
    meshes = get_meshes(meshnum, extent)

    # geojsonl文字列を生成
    geojsonl_txt = ""
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": []
        },
        "properties": {
            "code": ""
        }
    }
    for mesh in meshes:
        feature["geometry"]["coordinates"] = mesh["geometry"]
        feature["properties"]["code"] = mesh["code"]
        geojsonl_txt += json.dumps(feature) + "\n"

    print("writing file...")
    # geojsonl書き出し
    with open(os.path.join(target_dir, "mesh_" + str(meshnum) + ".geojsonl"), mode="w") as f:
        f.write(geojsonl_txt)

    print("done")
