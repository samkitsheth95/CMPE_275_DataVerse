import os
import helpers
import grpc
import fs_pb2 
import fs_pb2_grpc
from concurrent import futures
import time
import psutil
import shutil

class FileServer(fs_pb2_grpc.FileServerServicer):
    def __init__(self):

        root = "/home/samkit/cmpe275/Output/"
        filelist=[]
        for path, subdirs, files in os.walk(root):
            for name in files:
                filelist.append(name)
        
        class Servicer(fs_pb2_grpc.FileServerServicer):
            tmp_file_name = ''
            file_direc = '/home/samkit/cmpe275/Output/'

            def filename(self,req,context):
                print(filelist);
                if req.fn:
                    filelist.append(req.fn)
                    self.tmp_file_name=''
                    self.tmp_file_name=self.file_direc+req.fn
                return fs_pb2.fs(fn="done")
            
            def upload(self, request_iterator, context):
                helpers.save_chunks_to_file(request_iterator, self.tmp_file_name)
                return fs_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

            def download(self, request, context):
                if request.name and request.name in filelist:
                    self.tmp_file_name='/home/samkit/cmpe275/Output/'+request.name
                    return helpers.get_file_chunks(self.tmp_file_name)
                else:
                     msg = 'File not Found'
                     context.set_details(msg)
                     context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            
            def getServerStats(self, request, context):
                cpu_percent = str(psutil.cpu_percent())
                ram_stats = psutil.virtual_memory()._asdict()
                ram_total = str(ram_stats['total'])
                ram_available = str(ram_stats['available'])
                ram_percent = str(ram_stats['percent'])

                total_memory, used_memory, free_memory = shutil.disk_usage("/")

                return fs_pb2.stats(
                    cpuUtil = cpu_percent, ramTotal = str(ram_total),
                    ramAvailable = str(ram_available), ramPercent = str(ram_percent),
                    totalMemory = str(total_memory), usedMemory = str(used_memory),
                    freeMemory = str(free_memory)
                )
                
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

a = FileServer()
a.start(8000)