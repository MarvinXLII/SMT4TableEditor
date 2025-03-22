from .archive import Archive
from .files import File
from .tbl import TBL
from .spreadsheet import Spreadsheet


class TBB(Archive):
    def __init__(self, vanilla):
        self._vanilla = vanilla
        self.tables = []
        self._split_tables()
        self._modded = False


    @property
    def modded(self):
        return self._modded


    def _split_tables(self):
        f = File(self._vanilla)

        assert(f.read_string(size=4) == 'TBCR')
        start_addr = f.read_uint32()
        num_tables = f.read_uint32()
        table_pointers = []
        for i in range(num_tables):
            pointer = start_addr + f.read_uint32()
            table_pointers.append(pointer)

        f.seek(start_addr)
        i = 0
        for a, b in zip(table_pointers, table_pointers[1:]):
            assert(f.tell() == a)
            size = b - a
            data = bytearray(f.read_bytes(size))
            self.tables.append(TBL(data, i))
            i += 1
        assert(f.tell() == table_pointers[-1])
        data = bytearray(f.read_bytes())
        self.tables.append(TBL(data, i))


    def build(self):
        tables = bytearray()
        for table in self.tables:
            tables += table.get_data()
        num_tables = len(self.tables)
        start_addr = 4 * (num_tables + 3)
        if start_addr % 0x10:
            start_addr += 0x10 - (start_addr % 0x10)

        tbcr = bytearray()
        tbcr += b'TBCR'
        tbcr += int.to_bytes(start_addr, 4, 'little')
        tbcr += int.to_bytes(num_tables, 4, 'little')
        offset = 0
        for table in self.tables:
            tbcr += int.to_bytes(offset, 4, 'little')
            offset += table.data.size
        tbcr += bytearray([0] * (start_addr - len(tbcr)))

        tables = tbcr + tables

        if len(tables) != len(self._vanilla):
            self._modded = True
        else:
            for i, (t, v) in enumerate(zip(tables, self._vanilla)):
                if (t != v):
                    self._modded = True
                    break

        return tables


    def initialize_spreadsheets(self, filename):
        self._spreadsheet = Spreadsheet(filename, self)


    def load_spreadsheets(self):
        self._spreadsheet.load_spreadsheet()


    def dump_spreadsheets(self):
        self._spreadsheet.dump_spreadsheet()
