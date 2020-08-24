from unittest import TestCase
from japanmesh.main import *


class TestMain(TestCase):

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

        # 1次メッシュのメッシュコード
        self.assertEqual(get_mesh(1, 0, 0)["code"], "3022")
        self.assertEqual(get_mesh(1, 1, 0)["code"], "3023")
        self.assertEqual(get_mesh(1, 0, 1)["code"], "3122")
        self.assertEqual(get_mesh(1, 1, 1)["code"], "3123")

        # 2次メッシュ
        self.assertEqual(get_mesh(2, 0, 0)["code"], "302200")
        self.assertEqual(get_mesh(2, 1, 0)["code"], "302201")
        self.assertEqual(get_mesh(2, 0, 1)["code"], "302210")
        self.assertEqual(get_mesh(2, 1, 1)["code"], "302211")
        self.assertEqual(get_mesh(2, 7, 7)["code"], "302277")
        self.assertEqual(get_mesh(2, 8, 8)["code"], "312300")

        # 3次メッシュ
        self.assertEqual(get_mesh(3, 1, 1)["code"], "30220011")
        self.assertEqual(get_mesh(3, 9, 9)["code"], "30220099")
        self.assertEqual(get_mesh(3, 10, 10)["code"], "30221100")
        self.assertEqual(get_mesh(3, 79, 79)["code"], "30227799")
        self.assertEqual(get_mesh(3, 80, 80)["code"], "31230000")

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
