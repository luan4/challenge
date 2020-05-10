import json
from itertools import islice

# WARNING: if parser encouters empty lines, it raises error.

class Error(Exception):
   """Base class for other exceptions"""
   pass

class FileEndReached(Error):
   """Raised when parser reaches file end"""
   pass

class Parser:

    def __init__(self, file_name: str, file_formatting: dict, custom_formatting: dict, chunk_size: int=200):
        """ Stores config parameters in self and instantiates a generator object (input_fd) """

        self.file_name = file_name
        self.file_formatting = file_formatting
        self.custom_formatting = custom_formatting
        self.delimiter = self.custom_formatting.get("delimiter")
        self.chunk_size = chunk_size
        self.file_format = self.custom_formatting.get("format")
        self.input_fd = self.reader()

        #Skip header if it exists.
        if self.custom_formatting.get("header"):
            next(self.input_fd)


    def reader(self): 
        """ Returns a generator object which yields well formatted lines from input file """
        with open(self.file_name, **self.file_formatting) as f:
            if self.file_format == 'csv':
                for elem in f:
                    elem = elem.split(self.delimiter)
                    elem[1] = elem[1].rstrip("\n")
                    yield elem

            if self.file_format == 'jsonl':
                for elem in f:
                    elem = json.loads(elem)
                    elem = [elem["site"], elem["id"]]
                    yield elem

    def read_chunk(self) -> list:
        """ Makes use of reader (defined above) to return a list with 
            a chunk size number of lines """
        chunk = []
        for line in islice(self.input_fd, self.chunk_size):
            chunk.append(line)
        if not chunk:
            raise FileEndReached
        else:
            return chunk
