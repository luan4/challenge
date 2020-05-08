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
        self.input_fd = self.reader()

        #Skip header if it exists.
        if self.custom_formatting.get("header"):
            next(self.input_fd)

        self.delimiter = self.custom_formatting.get("delimiter")

        self.chunk_size = chunk_size


    def reader(self): 
        """ Returns a generator object which yields lines from input file """
        with open(self.file_name, **self.file_formatting) as f:
            for elem in f:
                yield elem

    def read_chunk(self) -> list:
        """ Returns a list with a chunk size number of lines """
        chunk = []
        for line in islice(self.input_fd, self.chunk_size):
            chunk.append(line.split(self.delimiter))
        if not chunk:
            raise FileEndReached
        else:
            return chunk

if __name__ == "__main__":

    with open("read_config.json", 'r') as config:
        data = json.load(config).get("items")

    file_formatting = data.get("file_formatting")
    custom_formatting = data.get("custom_formatting")

    parser = Parser("technical_challenge_data.csv", file_formatting, custom_formatting)
    for _ in range(4):
        print(parser.read_chunk())

