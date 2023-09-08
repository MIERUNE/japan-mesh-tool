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
        self.assertEqual(get_mesh(1, 12, 21)["code"], "5134")  # 高松
        self.assertEqual(get_mesh(1, 2, 6)["code"], "3624")  # 石垣
        self.assertEqual(get_mesh(1, 7, 12)["code"], "4229")  # 奄美
        self.assertEqual(get_mesh(1, 8, 19)["code"], "4930")  # 熊本
        self.assertEqual(get_mesh(1, 17, 23)["code"], "5339")  # 東京
        self.assertEqual(get_mesh(1, 20, 10)["code"], "4042")  # 父島
        self.assertEqual(get_mesh(1, 18, 24)["code"], "5440")  # 益子
        self.assertEqual(get_mesh(1, 18, 27)["code"], "5740")  # 仙台
        self.assertEqual(get_mesh(1, 19, 30)["code"], "6041")  # 八戸
        self.assertEqual(get_mesh(1, 20, 36)["code"], "6642")  # 士別
        self.assertEqual(get_mesh(1, 23, 34)["code"], "6445")  # 根室

        # 2次メッシュ
        self.assertEqual(get_mesh(2, 0, 0)["code"], "302200")
        self.assertEqual(get_mesh(2, 1, 0)["code"], "302201")
        self.assertEqual(get_mesh(2, 0, 1)["code"], "302210")
        self.assertEqual(get_mesh(2, 1, 1)["code"], "302211")
        self.assertEqual(get_mesh(2, 7, 7)["code"], "302277")
        self.assertEqual(get_mesh(2, 8, 8)["code"], "312300")
        self.assertEqual(get_mesh(2, 98, 174)["code"], "513462")  # 小豆島
        self.assertEqual(get_mesh(2, 116, 176)["code"], "523604")  # 津
        self.assertEqual(get_mesh(2, 117, 176)["code"], "523605")  # 津
        self.assertEqual(get_mesh(2, 116, 184)["code"], "533604")  # 岐阜
        self.assertEqual(get_mesh(2, 116, 185)["code"], "533614")  # 岐阜
        self.assertEqual(get_mesh(2, 17, 52)["code"], "362441")  # 石垣
        self.assertEqual(get_mesh(2, 60, 101)["code"], "422954")  # 奄美
        self.assertEqual(get_mesh(2, 69, 153)["code"], "493015")  # 熊本
        self.assertEqual(get_mesh(2, 142, 187)["code"], "533936")  # 東京
        self.assertEqual(get_mesh(2, 161, 81)["code"], "404211")  # 父島
        self.assertEqual(get_mesh(2, 144, 197)["code"], "544050")  # 益子
        self.assertEqual(get_mesh(2, 150, 216)["code"], "574006")  # 仙台
        self.assertEqual(get_mesh(2, 155, 246)["code"], "604163")  # 八戸
        self.assertEqual(get_mesh(2, 163, 290)["code"], "664223")  # 士別
        self.assertEqual(get_mesh(2, 186, 277)["code"], "644552")  # 根室

        # 3次メッシュ
        self.assertEqual(get_mesh(3, 0, 0)["code"], "30220000")
        self.assertEqual(get_mesh(3, 1, 1)["code"], "30220011")
        self.assertEqual(get_mesh(3, 9, 9)["code"], "30220099")
        self.assertEqual(get_mesh(3, 10, 10)["code"], "30221100")
        self.assertEqual(get_mesh(3, 79, 79)["code"], "30227799")
        self.assertEqual(get_mesh(3, 80, 80)["code"], "31230000")
        self.assertEqual(get_mesh(3, 988, 1741)["code"], "51346218")  # 小豆島
        self.assertEqual(get_mesh(3, 175, 525)["code"], "36244155")  # 石垣
        self.assertEqual(get_mesh(3, 607, 1012)["code"], "42295427")  # 奄美
        self.assertEqual(get_mesh(3, 694, 1534)["code"], "49301544")  # 熊本
        self.assertEqual(get_mesh(3, 1425, 1875)["code"], "53393655")  # 東京
        self.assertEqual(get_mesh(3, 1611, 812)["code"], "40421121")  # 父島
        self.assertEqual(get_mesh(3, 1446, 1972)["code"], "54405026")  # 益子
        self.assertEqual(get_mesh(3, 1508, 2162)["code"], "57400628")  # 仙台
        self.assertEqual(get_mesh(3, 1557, 2467)["code"], "60416377")  # 八戸
        self.assertEqual(get_mesh(3, 1635, 2904)["code"], "66422345")  # 士別
        self.assertEqual(get_mesh(3, 1864, 2776)["code"], "64455264")  # 根室

        # 4分割地域メッシュ
        self.assertEqual(get_mesh(4, 0, 0)["code"], "302200001")
        self.assertEqual(get_mesh(4, 1, 0)["code"], "302200002")
        self.assertEqual(get_mesh(4, 0, 1)["code"], "302200003")
        self.assertEqual(get_mesh(4, 1, 1)["code"], "302200004")
        self.assertEqual(get_mesh(4, 2, 2)["code"], "302200111")
        self.assertEqual(get_mesh(4, 1976, 3483)["code"], "513462183")  # 小豆島
        self.assertEqual(get_mesh(4, 351, 1051)["code"], "362441554")  # 石垣
        self.assertEqual(get_mesh(4, 1214, 2025)["code"], "422954273")  # 奄美
        self.assertEqual(get_mesh(4, 1389, 3068)["code"], "493015442")  # 熊本
        self.assertEqual(get_mesh(4, 2850, 3750)["code"], "533936551")  # 東京
        self.assertEqual(get_mesh(4, 3222, 1624)["code"], "404211211")  # 父島
        self.assertEqual(get_mesh(4, 2893, 3944)["code"], "544050262")  # 益子
        self.assertEqual(get_mesh(4, 3016, 4325)["code"], "574006283")  # 仙台
        self.assertEqual(get_mesh(4, 3115, 4935)["code"], "604163774")  # 八戸
        self.assertEqual(get_mesh(4, 3270, 5808)["code"], "664223451")  # 士別
        self.assertEqual(get_mesh(4, 3729, 5552)["code"], "644552642")  # 根室

        # 5分割地域メッシュ
        self.assertEqual(get_mesh(5, 703, 2103)["code"], "3624415544")  # 石垣
        self.assertEqual(get_mesh(5, 2428, 4051)["code"], "4229542733")  # 奄美
        self.assertEqual(get_mesh(5, 2779, 6136)["code"], "4930154422")  # 熊本
        self.assertEqual(get_mesh(5, 5700, 7500)["code"], "5339365511")  # 東京
        self.assertEqual(get_mesh(5, 6445, 3248)["code"], "4042112112")  # 父島
        self.assertEqual(get_mesh(5, 5786, 7889)["code"], "5440502623")  # 益子
        self.assertEqual(get_mesh(5, 6033, 8651)["code"], "5740062834")  # 仙台
        self.assertEqual(get_mesh(5, 6230, 9871)["code"], "6041637743")  # 八戸
        self.assertEqual(get_mesh(5, 6541, 11616)["code"], "6642234512")  # 士別
        self.assertEqual(get_mesh(5, 7458, 11105)["code"], "6445526423")  # 根室
        self.assertEqual(get_mesh(5, 3952, 6966)["code"], "5134621831")  # 小豆島

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
