from functools import lru_cache
import os
import math

try:
    from constants import (
        MESH_INFOS,
        FIRST_MESH_SIZE,
        MINIMUM_LAT,
        MINIMUM_LON,
        MAXIMUM_LAT,
        MAXIMUM_LON
    )
except ModuleNotFoundError:
    from .constants import (
        MESH_INFOS,
        FIRST_MESH_SIZE,
        MINIMUM_LAT,
        MINIMUM_LON,
        MAXIMUM_LAT,
        MAXIMUM_LON
    )


@lru_cache(maxsize=None)
def get_meshsize(meshnum: int) -> [float, float]:
    if meshnum == 1:
        return FIRST_MESH_SIZE

    meshinfo = MESH_INFOS[meshnum]
    parent_meshsize = get_meshsize((meshinfo["parent"]))
    meshsize = [
        parent_meshsize[0] / meshinfo["ratio"],
        parent_meshsize[1] / meshinfo["ratio"],
    ]
    return meshsize


def get_start_offset(meshnum: int, lonlat: list) -> tuple:
    """[summary]
    メッシュ次数と経緯度に対し、原点（左下）から数えて何個のメッシュをスキップするか計算
    Args:
        meshnum (int): メッシュ次数
        lonlat ([float, float]): [経度, 緯度]

    Returns:
        tuple: (x方向のオフセット、y方向のオフセット)
    """
    x_mesh_dist, y_mesh_dist = get_meshsize(meshnum)

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
    x_mesh_dist, y_mesh_dist = get_meshsize(meshnum)

    x_offset = 0
    while lonlat[0] <= MAXIMUM_LON - x_mesh_dist * (x_offset + 1):
        x_offset += 1

    y_offset = 0
    while lonlat[1] <= MAXIMUM_LAT - y_mesh_dist * (y_offset + 1):
        y_offset += 1

    return x_offset, y_offset


def get_meshes(meshnum: int, extent=None) -> list:
    """[summary]
    ジェネレータではなく通常のループで一度にすべてのメッシュ情報を取り出す関数
    メモリ使用量などを考慮する場合generate_meshes()を使用してください

    Args:
        meshnum (int): メッシュ次数
        extent (list, optional):  経緯度のペアのリストで領域指定

    Return:
        [{"geometry":<メッシュのジオメトリ>, "code":<メッシュコード>}...]
    """
    meshes = []
    for mesh in generate_meshes(meshnum, extent):
        meshes.append(mesh)
    return meshes


def generate_meshes(meshnum: int, extent=None):
    """[summary]
    メッシュ次数および領域から、その領域に重なる全てのメッシュの情報をリストで返す

    Args:
        meshnum (int): メッシュ次数
        extent (list, optional):  経緯度のペアのリストで領域指定

    yield:
        {"geometry":<メッシュのジオメトリ>, "code":<メッシュコード>}...
    """

    # メッシュのx方向y方向それぞれの数
    x_size, y_size = get_meshsize(meshnum)
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

    for y in range(start_offset[1], y_mesh_count - end_offset[1]):
        for x in range(start_offset[0], x_mesh_count - end_offset[0]):
            yield get_mesh(meshnum, x, y)


@lru_cache(maxsize=None)
def get_meshcode(meshnum: int, x: int, y: int) -> str:
    # 2次メッシュコード以降、メッシュ次数に応じてコードを2桁ずつ付加
    # 1-3:標準地域メッシュ
    # 4-6:分割地域メッシュ
    # 7以降:その他
    ratio = MESH_INFOS[meshnum]["ratio"]
    parent = MESH_INFOS[meshnum]["parent"]
    if meshnum == 1:
        # 1次コード：緯度を1.5倍した整数値 + 経度の整数部分の下2桁
        return ""
    elif meshnum == 4 or meshnum == 5 or meshnum == 6:
        return get_meshcode(parent, math.floor(x / ratio), math.floor(y / ratio)) + str((y % ratio) * 2 + (x % ratio) + 1)
    else:
        return get_meshcode(parent, math.floor(x / ratio), math.floor(y / ratio)) + str(y % ratio) + str(x % ratio)


@ lru_cache(maxsize=None)
def get_mesh_vertex(x: int, x_size: float, y: int, y_size: float) -> (float, float):
    return MINIMUM_LON + x * x_size, MINIMUM_LAT + y * y_size


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
    x_size, y_size = get_meshsize(meshnum)
    left_lon, bottom_lat = get_mesh_vertex(x, x_size, y, y_size)
    right_lon, top_lat = get_mesh_vertex(x + 1, x_size, y + 1, y_size)

    return {
        "geometry": [[
            [left_lon, bottom_lat],
            [left_lon, top_lat],
            [right_lon, top_lat],
            [right_lon, bottom_lat],
            [left_lon, bottom_lat]
        ]],
        "code": str(int(bottom_lat * 1.5)) + str(int(left_lon))[1:] + get_meshcode(meshnum, x, y)
    }


if __name__ == "__main__":
    import argschemes

    print("initializing...")
    # コマンド初期化
    args = argschemes.ARGSCHEME.parse_args()

    # メッシュ番号
    meshnum = args.meshnum
    # 別称での指定を次数に置き換え
    if meshnum == "500m":
        meshnum = 4
    elif meshnum == "250m":
        meshnum = 5
    elif meshnum == "125m":
        meshnum = 6
    elif meshnum == "100m":
        meshnum = 7
    elif meshnum == "50m":
        meshnum = 8
    elif meshnum == "10m":
        meshnum = 9
    elif meshnum == "5m":
        meshnum = 10
    else:
        try:
            meshnum = int(meshnum)
        except ValueError:
            raise ValueError(
                "メッシュ次数を正しく入力してください あなたの入力：" + str(args.meshnum))

    if meshnum < 1 or 10 < meshnum:
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
            for degree in latlon:
                if not -180 < degree < 180:
                    raise ValueError("経緯度は-180から180の間で指定してください")

    print("making meshes...")
    meshsize = get_meshsize(meshnum)
    # メッシュ生成
    meshes = []
    for mesh in generate_meshes(meshnum, extent):
        meshes.append(mesh)

    # geojsonl文字列を生成
    geojsonl_txt = ""
    for i in range(len(meshes)):
        geojsonl_txt += '{"type":"Feature","geometry":' + \
            '{"type":"Polygon","coordinates":' + \
            str(meshes[i]["geometry"]) + \
            '},"properties":{"code":' + meshes[i]["code"] + '}}\n'

    print("writing file...")
    # geojsonl書き出し
    with open(os.path.join(target_dir, "mesh_" + str(meshnum) + ".geojsonl"), mode="w") as f:
        f.write(geojsonl_txt)

    print("done")
