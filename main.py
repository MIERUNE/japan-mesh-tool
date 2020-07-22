import math
import json

#メッシュコード精製範囲
ORIGIN_MIN_LON = 122.00
ORIGIN_MAX_LON = 154.00
ORIGIN_MIN_LAT = 20.00
ORIGIN_MAX_LAT = 46.00

def get_mesh_offset(meshnum, lon, lat):
    x_mesh_dist, y_mesh_dist = get_mesh_size(meshnum)

    x_offset = 0
    while lon >= ORIGIN_MIN_LON + x_mesh_dist * (x_offset + 1):
        x_offset += 1

    y_offset = 0
    while lat >= ORIGIN_MIN_LAT + y_mesh_dist * (y_offset + 1):
        y_offset += 1

    return x_offset, y_offset

def get_mesh_size(meshnum):
    x_mesh_dist = 0
    y_mesh_dist = 0
    
    if meshnum == 1:
        x_mesh_dist = 1
        y_mesh_dist = 2/3
    # 2次メッシュ
    elif meshnum == 2:
        x_mesh_dist = 1/8
        y_mesh_dist = 1/12
    elif meshnum == 3:
        x_mesh_dist = 1/80
        y_mesh_dist = 1/120
    elif meshnum == 4:
        x_mesh_dist = 1/160
        y_mesh_dist = 1/240
    elif meshnum == 5:
        x_mesh_dist = 1/320
        y_mesh_dist = 1/480
    elif meshnum == 6:
        x_mesh_dist = 1/1600
        y_mesh_dist = 1/2400

    return x_mesh_dist, y_mesh_dist


def get_meshes(meshnum, extent=None)->list:
    x_mesh_dist, y_mesh_dist = get_mesh_size(meshnum)

    # メッシュのx方向y方向それぞれの数
    x_mesh_count = math.ceil((ORIGIN_MAX_LON - ORIGIN_MIN_LON) / x_mesh_dist)
    y_mesh_count = math.ceil((ORIGIN_MAX_LAT - ORIGIN_MIN_LAT) / y_mesh_dist)
    x_mesh_count = 100
    y_mesh_count = 100
    meshes = []
    for y in range(y_mesh_count):
        for x in range(x_mesh_count):
            leftbottom = [ORIGIN_MIN_LON + x * x_mesh_dist,
                            ORIGIN_MIN_LAT + y * y_mesh_dist]
            righttop = [ORIGIN_MIN_LON + (x + 1) * x_mesh_dist,
                            ORIGIN_MIN_LAT + (y + 1) * y_mesh_dist]
            mesh = [
                leftbottom,
                [leftbottom[0], righttop[1]],
                righttop,
                [righttop[0], leftbottom[1]],
                leftbottom
            ]
            meshes.append(mesh)
    return meshes




if __name__ == "__main__":
    geojsonl_txt = ""

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": []
        },
        "properties": {
            "id":"0"
        }
    }
    meshes = get_meshes(6)
    
    x_offset, y_offset = get_mesh_offset(1, 123, 20.6)
    print(x_offset, y_offset)
    """
    for mesh in meshes:
        feature["geometry"]["coordinates"] = [mesh]
        geojsonl_txt += json.dumps(feature, ensure_ascii=False) + "\n"

    with open("./1st.geojsonl", mode='w') as f:
        f.write(geojsonl_txt)
    """