from unittest import TestCase
from japanmesh.main import *


class TestMain(TestCase):
    def test_get_start_offset(self):
        # start_offset=(左から数えて完全に領域外となるx方向メッシュの数,
        # 下から数えて完全に領域外となるy方向メッシュの数,)
        self.assertEqual(get_start_offset(1, [122.0, 20.0]), (0, 0))
        self.assertEqual(get_start_offset(1, [123.0, 20.0]), (1, 0))
        self.assertEqual(get_start_offset(1, [123.0, 20.66666666666666]), (1, 0))
        self.assertEqual(get_start_offset(1, [123.0, 20.66666666666667]), (1, 1))

    def test_get_end_offset(self):
        # end_offset=(右から数えて完全に領域外となるx方向メッシュの数,
        # 上から数えて完全に領域外となるy方向メッシュの数,)
        self.assertEqual(get_end_offset(1, [154.0, 46.0]), (0, 0))
        self.assertEqual(get_end_offset(1, [153.0, 46.0]), (1, 0))
        self.assertEqual(get_end_offset(1, [153.0, 45.33333333333334]), (1, 0))
        self.assertEqual(get_end_offset(1, [153.0, 45.33333333333333]), (1, 1))

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
        self.assertEqual(get_mesh(1, 12, 21)["code"], "5134")
        self.assertEqual(get_mesh(1, 2, 6)["code"], "3624")
        self.assertEqual(get_mesh(1, 7, 12)["code"], "4229")
        self.assertEqual(get_mesh(1, 8, 19)["code"], "4930")
        self.assertEqual(get_mesh(1, 17, 23)["code"], "5339")
        self.assertEqual(get_mesh(1, 20, 10)["code"], "4042")
        self.assertEqual(get_mesh(1, 18, 24)["code"], "5440")
        self.assertEqual(get_mesh(1, 18, 27)["code"], "5740")
        self.assertEqual(get_mesh(1, 19, 30)["code"], "6041")
        self.assertEqual(get_mesh(1, 20, 36)["code"], "6642")
        self.assertEqual(get_mesh(1, 23, 34)["code"], "6445")

        # 2次メッシュ
        self.assertEqual(get_mesh(2, 0, 0)["code"], "302200")
        self.assertEqual(get_mesh(2, 1, 0)["code"], "302201")
        self.assertEqual(get_mesh(2, 0, 1)["code"], "302210")
        self.assertEqual(get_mesh(2, 1, 1)["code"], "302211")
        self.assertEqual(get_mesh(2, 7, 7)["code"], "302277")
        self.assertEqual(get_mesh(2, 8, 8)["code"], "312300")
        self.assertEqual(get_mesh(2, 98, 174)["code"], "513462")
        self.assertEqual(get_mesh(2, 116, 176)["code"], "523604")
        self.assertEqual(get_mesh(2, 117, 176)["code"], "523605")
        self.assertEqual(get_mesh(2, 116, 184)["code"], "533604")
        self.assertEqual(get_mesh(2, 116, 185)["code"], "533614")
        self.assertEqual(get_mesh(2, 17, 52)["code"], "362441")
        self.assertEqual(get_mesh(2, 60, 101)["code"], "422954")
        self.assertEqual(get_mesh(2, 69, 153)["code"], "493015")
        self.assertEqual(get_mesh(2, 142, 187)["code"], "533936")
        self.assertEqual(get_mesh(2, 161, 81)["code"], "404211")
        self.assertEqual(get_mesh(2, 144, 197)["code"], "544050")
        self.assertEqual(get_mesh(2, 150, 216)["code"], "574006")
        self.assertEqual(get_mesh(2, 155, 246)["code"], "604163")
        self.assertEqual(get_mesh(2, 163, 290)["code"], "664223")
        self.assertEqual(get_mesh(2, 186, 277)["code"], "644552")

        # 3次メッシュ
        self.assertEqual(get_mesh(3, 0, 0)["code"], "30220000")
        self.assertEqual(get_mesh(3, 1, 1)["code"], "30220011")
        self.assertEqual(get_mesh(3, 9, 9)["code"], "30220099")
        self.assertEqual(get_mesh(3, 10, 10)["code"], "30221100")
        self.assertEqual(get_mesh(3, 79, 79)["code"], "30227799")
        self.assertEqual(get_mesh(3, 80, 80)["code"], "31230000")
        self.assertEqual(get_mesh(3, 988, 1741)["code"], "51346218")
        self.assertEqual(get_mesh(3, 175, 525)["code"], "36244155")
        self.assertEqual(get_mesh(3, 607, 1012)["code"], "42295427")
        self.assertEqual(get_mesh(3, 694, 1534)["code"], "49301544")
        self.assertEqual(get_mesh(3, 1425, 1875)["code"], "53393655")
        self.assertEqual(get_mesh(3, 1611, 812)["code"], "40421121")
        self.assertEqual(get_mesh(3, 1446, 1972)["code"], "54405026")
        self.assertEqual(get_mesh(3, 1508, 2162)["code"], "57400628")
        self.assertEqual(get_mesh(3, 1557, 2467)["code"], "60416377")
        self.assertEqual(get_mesh(3, 1635, 2904)["code"], "66422345")
        self.assertEqual(get_mesh(3, 1864, 2776)["code"], "64455264")

        # 4~6:分割地域メッシュ
        self.assertEqual(get_mesh(4, 0, 0)["code"], "302200001")
        self.assertEqual(get_mesh(4, 1, 0)["code"], "302200002")
        self.assertEqual(get_mesh(4, 0, 1)["code"], "302200003")
        self.assertEqual(get_mesh(4, 1, 1)["code"], "302200004")
        self.assertEqual(get_mesh(4, 2, 2)["code"], "302200111")
        self.assertEqual(get_mesh(4, 1976, 3483)["code"], "513462183")

        # 7~:その他メッシュ
        self.assertEqual(get_mesh(7, 0, 0)["code"], "3022000000")
        self.assertEqual(get_mesh(7, 0, 1)["code"], "3022000010")
        self.assertEqual(get_mesh(7, 1, 0)["code"], "3022000001")
        self.assertEqual(get_mesh(7, 1, 1)["code"], "3022000011")
        self.assertEqual(get_mesh(7, 9, 9)["code"], "3022000099")
        self.assertEqual(get_mesh(7, 10, 10)["code"], "3022001100")

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
