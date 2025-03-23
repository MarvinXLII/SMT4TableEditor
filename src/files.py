import sys
from pathlib import Path
import struct
import bsdiff4
import io


class Byte:
    @staticmethod
    def get_int8(value):
        return struct.pack("<b", value)

    @staticmethod
    def get_uint8(value):
        return struct.pack("<B", value)

    @staticmethod
    def get_int16(value):
        return struct.pack("<h", value)

    @staticmethod
    def get_uint16(value):
        return struct.pack("<H", value)

    @staticmethod
    def get_int32(value):
        return struct.pack("<l", value)

    @staticmethod
    def get_uint32(value):
        return struct.pack("<L", value)

    @staticmethod
    def get_int64(value):
        return struct.pack("<q", value)

    @staticmethod
    def get_uint64(value):
        return struct.pack("<Q", value)

    @staticmethod
    def get_float(value):
        return struct.pack("<f", value)

    @staticmethod
    def get_double(value):
        return struct.pack("<d", value)

    @staticmethod
    def get_string(string, nbytes):
        encoded = bytearray()
        for si in string:
            ei = si.encode('utf8')
            if ei[0] & 0x80:
                ei = si.encode('shift-jis')
            encoded += ei
        assert(nbytes >= len(encoded))
        encoded += bytearray([0] * (nbytes - len(encoded)))
        return encoded


class File(Byte):
    def __init__(self, data):
        self.vanilla = bytearray(data)
        self.size = len(self.vanilla)
        self.data = io.BytesIO(self.vanilla);

    def get_data(self):
        return bytearray(self.data.getbuffer())

    def tell(self):
        return self.data.tell()

    def seek(self, offset, x=0):
        self.data.seek(offset, x)

    def read_bytes(self, size=None):
        if size is None:
            return self.data.read()
        return self.data.read(size)

    def read_string(self, size):
        s = self.read_bytes(size)
        try:
            return s.rstrip(b'\x00').decode('utf8')
        except:
            pass

        decoded = []
        i = 0
        while i < len(s) and s[i] != 0:
            if s[i] & 0x80:
                si = s[i:i+2].decode('shift-jis')
                i += 2
            else:
                si = s[i:i+1].decode('utf8')
                i += 1
            decoded.append(si)

        return ''.join(decoded)

    def read_int(self, size, signed):
        return int.from_bytes(self.data.read(size), byteorder='little', signed=signed)

    def read_int8(self):
        return self.read_int(1, True)

    def read_int16(self):
        return self.read_int(2, True)

    def read_int32(self):
        return self.read_int(4, True)

    def read_int64(self):
        return self.read_int(8, True)

    def read_uint8(self):
        return self.read_int(1, False)

    def read_uint16(self):
        return self.read_int(2, False)

    def read_uint32(self):
        return self.read_int(4, False)

    def read_uint64(self):
        return self.read_int(8, False)

    def read_float(self):
        return struct.unpack("<f", self.data.read(4))[0]

    def read_double(self):
        return struct.unpack("<d", self.data.read(8))[0]
