import os
from concurrent import futures

import grpc
import time
import fs_pb2 
import fs_pb2_grpc


CHUNK_SIZE = 1024 * 1024  # 1MB


def get_file_chunks(filename):
    try:
        with open(filename, 'rb') as f:
            while True:
                piece = f.read(CHUNK_SIZE);
                if len(piece) == 0:
                    return
                yield fs_pb2.Chunk(buffer=piece)
    except FileNotFoundError:
        print("Wrong file path")


def save_chunks_to_file(chunks, filename):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)