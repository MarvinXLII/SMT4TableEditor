import bsdiff4
import lzma

from .tbb import TBB
from .fbin import FBIN
from .utilities import shrink_path



def load_archive(filename):
    with filename.open('rb') as file:
        magic = file.read(4)

    if magic == b'TBCR':
        assert(filename.suffix == '.tbb')
        data = load_file(filename)
        return TBB(data)
    elif magic == b'FBIN':
        assert(filename.suffix == '.bin')
        data = load_file(filename)
        return FBIN(data)

    print('Not setup for', filename)
    return None



def load_file(filename):
    print('Loading', filename)
    data = bytearray(filename.open('rb').read())

    patchfile = 'patches' / shrink_path(filename).with_suffix('.xz')
    if patchfile.exists():
        print('Patching', patchfile)
        with lzma.open(patchfile, 'rb') as file:
            patch = bytearray(file.read())
            data = bsdiff4.patch(bytes(data), bytes(patch))

    return data
