import os
import helpers
import grpc
import fs_pb2 
import fs_pb2_grpc
from concurrent import futures
import time

class FileServer(fs_pb2_grpc.FileServerServicer):
    def __init__(self):
        class Servicer(fs_pb2_grpc.FileServerServicer):
            filessaved = []
            tmp_file_name = ''
            file_direc = '/home/samkit/cmpe275/Output/'
            def filename(self,req,context):
                if req.fn:
                    self.filessaved.append(req.fn)
                    self.tmp_file_name=''
                    self.tmp_file_name=self.file_direc+req.fn
                return fs_pb2.fs(fn="done")
            
            def upload(self, request_iterator, context):
                helpers.save_chunks_to_file(request_iterator, self.tmp_file_name)
                return fs_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

            def download(self, request, context):
                if request.name and request.name in self.filessaved:
                    self.tmp_file_name='/home/samkit/cmpe275/Output/'+request.name
                    return helpers.get_file_chunks(self.tmp_file_name)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        fs_pb2_grpc.add_FileServerServicer_to_server(Servicer(), self.server)

    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)

a= FileServer()
a.start(8888)

