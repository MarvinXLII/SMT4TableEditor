from pathlib import Path


TITLE_ID_SMT4 = '00040000000E5C00'
TITLE_ID_SMT4_APOC = '000400000019A200'


def shrink_path(filename):
    parts = list(filename.resolve().parts)
    try:
        idx = parts.index(TITLE_ID_SMT4)
    except ValueError:
        try:
            idx = parts.index(TITLE_ID_SMT4_APOC)
        except ValueError:
            print('Title ID must be in the file path of the .tbb file!')
            print('    SMT IV:', TITLE_ID_SMT4)
            print('    SMT IV Apocalypse:', TITLE_ID_SMT4_APOC)
            exit(-1)
    if parts[idx+1] == 'romfs':
        parts.remove('romfs')
    return Path(*parts[idx:])
