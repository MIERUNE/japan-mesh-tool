from unittest import TestCase
from py_src.main import *


class TestMain(TestCase):

    def test_get_mesh_size(self):
        # 1次メッシュのメッシュ1枚のサイズは(lon, lat) = (1.0, 2.0/3.0)
        self.assertEqual(get_mesh_size(1), (1.0, 2.0/3.0))

    def test_get_start_offset(self):
        # start_offset=(左から数えて完全に領域外となるx方向メッシュの数,
        # 下から数えて完全に領域外となるy方向メッシュの数,)
        self.assertEqual(get_start_offset(1, [122.0, 20.0]), (0, 0))
        self.assertEqual(get_start_offset(1, [123.0, 20.0]), (1, 0))
        self.assertEqual(get_start_offset(
            1, [123.0, 20.66666666666666]), (1, 0))
        self.assertEqual(get_start_offset(
            1, [123.0, 20.66666666666667]), (1, 1))

    def test_get_end_offset(self):
        # end_offset=(右から数えて完全に領域外となるx方向メッシュの数,
        # 上から数えて完全に領域外となるy方向メッシュの数,)
        self.assertEqual(get_end_offset(1, [154.0, 46.0]), (0, 0))
        self.assertEqual(get_end_offset(1, [153.0, 46.0]), (1, 0))
        self.assertEqual(get_end_offset(
            1, [153.0, 45.33333333333334]), (1, 0))
        self.assertEqual(get_end_offset(
            1, [153.0, 45.33333333333333]), (1, 1))

    def test_get_mesh(self):
        mesh = get_mesh(1, 0, 0)
        # mesheにはメッシュコードとポリゴンのジオメトリが格納されている
        # ジオメトリはgeojson準拠:[[lon,lat],[lon,lat],[lon,lat],[lon,lat],[lon,lat]]
        self.assertEqual(len(mesh["geometry"][0]), 5)
        # メッシュコードの割り振り規則は後述
        self.assertEqual(mesh["code"], "3022")

    def test_get_meshes(self):
        # 1次メッシュを計算
        meshes = get_meshes(1)

        # 1次メッシュは32x39=1248
        self.assertEqual(len(meshes), 1248)
        # 領域を指定して生成する
        # 前述のテストから、start_offset=(1, 1)、end_offset=(1, 1)であるから
        # メッシュ数は30x37=1110となる
        meshes_with_offset = get_meshes(1, [[123.0, 20.7], [153.0, 45.3]])
        self.assertEqual(len(meshes_with_offset), 1110)

    def test_get_meshcode(self):
        # get_meshcode(meshnum, x, y)
        # meshnumはメッシュ次数、x, yは左下から数えたメッシュの番地

        # 1次メッシュのメッシュコード
        self.assertEqual(get_meshcode(1, 0, 0), "3022")
        self.assertEqual(get_meshcode(1, 1, 0), "3023")
        self.assertEqual(get_meshcode(1, 0, 1), "3122")
        self.assertEqual(get_meshcode(1, 1, 1), "3123")

        # 2次メッシュ
        self.assertEqual(get_meshcode(2, 0, 0), "302200")
        self.assertEqual(get_meshcode(2, 1, 0), "302201")
        self.assertEqual(get_meshcode(2, 0, 1), "302210")
        self.assertEqual(get_meshcode(2, 1, 1), "302211")
        self.assertEqual(get_meshcode(2, 7, 7), "302277")
        self.assertEqual(get_meshcode(2, 8, 8), "312300")

        # 3次メッシュ
        self.assertEqual(get_meshcode(3, 1, 1), "30220011")
        self.assertEqual(get_meshcode(3, 9, 9), "30220099")
        self.assertEqual(get_meshcode(3, 10, 10), "30221100")
        self.assertEqual(get_meshcode(3, 79, 79), "30227799")
        self.assertEqual(get_meshcode(3, 80, 80), "31230000")

        # 4次以降上記と同じ法則でコードを割り振り
