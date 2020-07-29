import argparse

ARGSCHEME = argparse.ArgumentParser(
    description='地域メッシュを生成するスクリプト')
ARGSCHEME.add_argument('meshnum', help='メッシュ次数')
ARGSCHEME.add_argument('-e', '--extent', nargs=2,
                       help='メッシュを生成する領域のカンマ区切り経緯度（オプション）')
ARGSCHEME.add_argument('-d', '--target_dir', help='データの保存先（オプション）')
