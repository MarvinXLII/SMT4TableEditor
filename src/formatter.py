import sys
from pathlib import Path
from .files import File, Byte
from enum import Enum
import json
import shutil


class Format(str, Enum):
    BOOL = 'bool'
    UINT8 = 'uint8'
    UINT16 = 'uint16'
    UINT32 = 'uint32'
    UINT64 = 'uint64'
    INT8 = 'int8'
    INT16 = 'int16'
    INT32 = 'int32'
    INT64 = 'int64'
    FLOAT = 'float'


class Formatter:
    def __init__(self, filepath):
        self._data = dict()
        self._header = dict()
        self._sheet_name = filepath.stem
        if filepath.exists():
            print('Loading', filepath)
            data = json.load(filepath.open('r'))
            if 'types' in data:
                self._data = {int(k, 0x10) : v for k, v in data['types'].items()}
            if 'headers' in data:
                self._header = {int(k, 0x10) : v for k, v in data['headers'].items()}
            if 'sheetname' in data:
                self._sheet_name = data['sheetname']
                if self._sheet_name != filepath.stem:
                    index = filepath.stem.split('_')[1]
                    self._sheet_name = index + ' ' + self._sheet_name
                if len(self._sheet_name) > 31:
                    print('Sheet names number be less than', 31 - len(index), 'characters')
                    print(data['sheetname'], 'has', len(data['sheetname']), 'characters')
                    print('Shorten it in', filepath)
                    exit(-1)

    @property
    def sheet_name(self):
        return self._sheet_name        

    def read(self, table, offset):
        addr = table.tell()
        if offset in self._data:
            if self._data[offset].startswith('string_'):
                n = self._data[offset].split('_')[1]
                try:
                    n = int(n)
                except:
                    n = int(n, 0x10)
                return table.read_string(n)
            
            match self._data[offset]:
                case Format.UINT8:
                    return table.read_uint8()
                case Format.UINT16:
                    return table.read_uint16()
                case Format.UINT32:
                    return table.read_uint32()
                case Format.UINT64:
                    return table.read_uint64()
                case Format.INT8:
                    return table.read_int8()
                case Format.INT16:
                    return table.read_int16()
                case Format.INT32:
                    return table.read_int32()
                case Format.INT64:
                    return table.read_int64()
                case Format.FLOAT:
                    return table.read_float()
                case _:
                    return table.read_uint8()
        else:
            return table.read_uint8()


    def get(self, value, offset):
        if offset in self._data:
            if self._data[offset].startswith('string_'):
                n = self._data[offset].split('_')[1]
                try:
                    n = int(n)
                except:
                    n = int(n, 0x10)
                # ensure value is a string (e.g. replacing script with '0' can be read as an integer!)
                return Byte.get_string(str(value), n)
            
            match self._data[offset]:
                case Format.UINT8:
                    return Byte.get_uint8(value)
                case Format.UINT16:
                    return Byte.get_uint16(value)
                case Format.UINT32:
                    return Byte.get_uint32(value)
                case Format.UINT64:
                    return Byte.get_uint64(value)
                case Format.INT8:
                    return Byte.get_int8(value)
                case Format.INT16:
                    return Byte.get_int16(value)
                case Format.INT32:
                    return Byte.get_int32(value)
                case Format.INT64:
                    return Byte.get_int64(value)
                case Format.FLOAT:
                    return Byte.get_float(value)
                case _:
                    return Byte.get_uint8(value)
        else:
            return Byte.get_uint8(value)


    def header(self, value):
        try:
            v = int(value, 0x10)
        except:
            print("Poor header format in json")
            print("    ", value)
            return ""
        if v in self._header:
            return self._header[v]
        return ""
