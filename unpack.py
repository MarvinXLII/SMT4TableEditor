import os
from pathlib import Path

from src import *


def print_failed_files(failed):
    failfile = Path('failed.txt')
    if failfile.exists():
        os.remove(failfile)
    if failed:
        print('')
        print('Failed files:')
        failed.sort()
        with failfile.open('w') as file:
            for f in failed:
                print('  ', f)
                file.write(str(f) + '\n')


if __name__ == '__main__':
    cmdargs = get_cmd_line_args()
    table_files = get_input_files(cmdargs.args)
    bin_files = get_bin_files(cmdargs.args)

    failed = []

    for filename in table_files + bin_files:
        print('')

        try:
            archive = load_archive(filename)
        except:
            failed.append(filename)
            continue

        if archive:
            archive.initialize_spreadsheets(filename)
            archive.dump_spreadsheets()

    print_failed_files(failed)
