import os
import helpers
import grpc
import fs_pb2 
import fs_pb2_grpc
import random

class client:
    def __init__(self, server):
        channel = grpc.insecure_channel(server)
        self.stub = fs_pb2_grpc.FileServerStub(channel)

    def sendfile(self, in_file_name,fn):
        try:
            responseq = self.stub.filename(fs_pb2.fs(fn=fn))
            print(responseq)
            chunks_generator = helpers.get_file_chunks(in_file_name)
            response = self.stub.upload(chunks_generator)
            assert response.length == os.path.getsize(in_file_name)
        except grpc.RpcError as e:
            print(e.details())
        except FileNotFoundError:
            print("Wrong file path")
    def getfile(self, target_name, out_file_name):
        try:
            response = self.stub.download(fs_pb2.Request(name=target_name))
            helpers.save_chunks_to_file(response, out_file_name)  
            return True
        except grpc.RpcError as e:
            print(e.details())
            return False
try:
    while True:
        option = input("press 1 to store file or 2 to search file ")
        servers = ['localhost:8000','localhost:8001','localhost:8002','localhost:8003']
        selecttwo = random.sample(range(0, len(servers)), 2)
        conn=[]
        for server in servers:
            conn.append(client(server))
        a = client('localhost:8000')

        if option=="1":
            in_file_name = input("Enter FilePath ")
            fn = in_file_name.rsplit('/',1)[1]
            print(fn)
            conn[selecttwo[0]].sendfile(in_file_name,fn)
            conn[selecttwo[1]].sendfile(in_file_name,fn)
            # a.sendfile(in_file_name,fn)
            # a1.sendfile(in_file_name,fn)
        else:
            searchfile = input("Enter FileSearch ")
            check=True
            for connection in conn:
                if connection.getfile(searchfile,"/home/samkit/cmpe275/Input/"+searchfile):
                    print('file found!')
                    check=False
                    break
            if check: print('file not found!')
            # if a.getfile(searchfile,"/home/samkit/cmpe275/Input/"+searchfile):
            #     print('found s1')            
except KeyboardInterrupt:
        exit()

    # demo for file downloading:
    # out_file_name = '/home/samkit/cmpe275/IN/sam'
    # if os.path.exists(out_file_name):
    #     os.remove(out_file_name)
    # client.download('whatever_name', out_file_name)
    # os.system(f'sha1sum {in_file_name}')
    # os.system(f'sha1sum {out_file_name}')