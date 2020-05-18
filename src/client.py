import os
import helpers
import grpc
import fs_pb2 
import fs_pb2_grpc
import random
from dotenv import load_dotenv
import os

load_dotenv();

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
    def getServerStats(self):
        try:
            response = self.stub.getServerStats(fs_pb2.EMPTY())
            return response
        except grpc.RpcError as e:
            print(e.details())
            return "Server is down"
try:
    while True:
        option = input("press 1 to store file, 2 to search file or 3 to get status\n")
        servers = os.getenv("CLIENT_SERVER_LIST").split(',')
        selecttwo = random.sample(range(0, len(servers)), 2)
        conn=[]
        for server in servers:
            conn.append(client(server))

        if option=="1":
            in_file_name = input("Enter FilePath ")
            fn = in_file_name.rsplit('/',1)[1]
            print(fn)
            conn[selecttwo[0]].sendfile(in_file_name,fn)
            conn[selecttwo[1]].sendfile(in_file_name,fn)
        elif option=="2":
            searchfile = input("Enter FileSearch ")
            check=True
            for connection in conn:
                if connection.getfile(searchfile,os.getenv("CLIENT_FILE_OUTPUT")+searchfile):
                    print('file found!')
                    check=False
                    break
            if check: print('file not found!')
        elif option=="3":
            for index, connection in enumerate(conn):
                status = connection.getServerStats()
                print("\nStatus for server " + servers[index] + ":")
                print(status)
except KeyboardInterrupt:
        exit()