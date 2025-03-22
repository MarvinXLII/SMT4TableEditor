from pathlib import Path

from .archive import Archive
from .files import File
from .spreadsheet import Spreadsheet
from .tbb import TBB


class FBIN(Archive):
    def __init__(self, vanilla):
        self._vanilla = vanilla
        self._tbb = self._split_tables()
        self._spreadsheets = []
        self._modded = False


    @property
    def modded(self):
        return self._modded
        

    def _split_tables(self):
        f = File(self._vanilla)
        assert(f.read_string(size=4) == 'FBIN')

        num_tables = f.read_uint32()
        start_addr = f.read_uint32()

        sizes = []
        for _ in range(num_tables):
            sizes.append(f.read_uint32())
        assert(f.tell() == start_addr)

        tbb = []
        for size in sizes:
            data = f.read_bytes(size)
            tbb.append(TBB(data))

        return tbb
        

    def initialize_spreadsheets(self, filename):
        for i, tbb in enumerate(self._tbb):
            p = Path(filename.parent, f'{filename.stem}_{i}.tbb')
            spreadsheet = Spreadsheet(p, tbb)
            self._spreadsheets.append(spreadsheet)


    def dump_spreadsheets(self):
        for spreadsheet in self._spreadsheets:
            spreadsheet.dump_spreadsheet()


    def load_spreadsheets(self):
        for spreadsheet in self._spreadsheets:
            spreadsheet.load_spreadsheet()


    def build(self):
        fbin = bytearray()
        fbin += b'FBIN'
        start_addr = 4 * (3 + len(self._tbb))
        fbin += int.to_bytes(len(self._tbb), 4, 'little')
        fbin += int.to_bytes(start_addr, 4, 'little')
        data = []
        self._modded = False
        for i, tbb in enumerate(self._tbb):
            data.append(tbb.build())
            self._modded |= tbb.modded
            fbin += int.to_bytes(len(data[-1]), 4, 'little')
        assert(len(fbin) == start_addr)
        for d in data:
            fbin += d
        return fbin
