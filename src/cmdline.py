import argparse


def get_cmd_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*', help="input directories and/or *.tbb files")
    return parser.parse_args()
