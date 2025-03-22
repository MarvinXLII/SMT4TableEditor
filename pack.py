import os
from pathlib import Path

from unpack import print_failed_files
from src import *


def dump_modded_file(filename, data):
    parts = list(shrink_path(filename).parts)
    parts.insert(1, 'romfs')
    outfile = 'mods' / Path(*parts)
    print('Dumping modded', outfile)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open('wb') as file:
        file.write(data)
    return outfile


if __name__ == '__main__':
    cmdargs = get_cmd_line_args()
    table_files = get_input_files(cmdargs.args)
    bin_files = get_bin_files(cmdargs.args)

    failed = []
    modded = []

    for filename in table_files + bin_files:
        print('')
        try:
            archive = load_archive(filename)
        except:
            failed.append(filename)
            continue

        if archive:
            archive.initialize_spreadsheets(filename)
            archive.load_spreadsheets()
            print('Building', filename)
            data = archive.build()
            if archive.modded:
                outfile = dump_modded_file(filename, data)
                modded.append(outfile)
            else:
                print('Skipping unmodded file')

    print('')
    if modded:
        modded.sort()
        print('modded files:')
        for m in modded:
            print('   ', m)
    else:
        print('No files modded')

    print_failed_files(failed)
