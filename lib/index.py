import os
import struct

class Index:
    def __init__(self, indexFile, dataFile):
        size = os.path.getsize(indexFile)
        assert size % 24 == 0, "Index file '%s' is not a multiple of 24 bytes in length" % size
        self.top        = (size / 24) - 1
        self.index      = open(indexFile, "rb")
        self.data       = open(dataFile,  "r")
        self.entries    = {}
        self.entries[0] = struct.unpack(">QQQ", self.index.read(24))
        self.first      = self.entries[0][0]
        self.last       = self.read(self.top)[0]

    # Read a 24 byte entry [0..top] from the index and return the entry as a triple of integers
    def read(self, entry):
        self.index.seek(entry * 24)    # Seek to the entry
        self.entries[entry] = struct.unpack(">QQQ", self.index.read(24))
        return self.entries[entry]

    # Search the index for a value using a binary search and cacheing the entries
    def find(self, key, bottom, top):
        middle = int((bottom + top) / 2)

        # If entry is not in the cache, read it
        if middle not in self.entries:
            self.read(middle)

        # Found it
        if key == self.entries[middle][0]:
            return self.entries[middle]

        # Key is before middle
        if key < self.entries[middle][0]:
            if bottom == middle:
                return None

            return self.find(key, bottom, middle - 1)

        # Degenerate case of bottom == top
        if middle == top:
            return None

        return self.find(key, middle + 1, top)

    def get(self, key):
        if key < self.first:
            raise KeyError("Key %d comes before first key in the index %d" % (key, self.first))

        if key > self.last:
            raise KeyError("Key %d comes after last key in the index %d" % (key, self.last))

        entry = self.find(key, 0, self.top)

        if entry == None:
            raise KeyError("Key %d not found in index" % key)

        self.data.seek(entry[1])
        return self.data.read(entry[2])

