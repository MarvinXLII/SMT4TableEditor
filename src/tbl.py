from .files import File


class TBL:
    def __init__(self, data, index):
        self.data = File(data)
        self._index = index
        assert(self.data.read_string(size=4) == 'TBL1')
        self.size = self.data.read_uint32()
        self.row_size = self.data.read_uint32()
        self.start_addr = self.data.read_uint32()
        assert(self.size % self.row_size == 0)

    @property
    def num_rows(self):
        return self.size // self.row_size


    @property
    def index(self):
        return self._index


    def build(self, data):
        new_data = bytearray()
        assert(len(data) % self.row_size == 0)

        self.size = len(data)
        header = bytearray()
        header += b'TBL1'
        header += int.to_bytes(self.size, 4, 'little')
        header += int.to_bytes(self.row_size, 4, 'little')
        header += int.to_bytes(self.start_addr, 4, 'little')
        assert(len(header) == 0x10)

        data = header + data
        if len(data) % 0x10:
            n = 0x10 - (len(data) % 0x10)
            data += bytearray([0] * n)
        
        self.data = File(data)


    def get_data(self):
        self.data.seek(0)
        return self.data.read_bytes()
