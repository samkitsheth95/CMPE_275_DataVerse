import os
import helpers
import grpc
import fs_pb2 
import fs_pb2_grpc

class client:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:8888')
        self.stub = fs_pb2_grpc.FileServerStub(channel)

    def sendfile(self, in_file_name,fn):
        responseq = self.stub.filename(fs_pb2.fs(fn=fn))
        print(responseq)
        chunks_generator = helpers.get_file_chunks(in_file_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)

    def getfile(self, target_name, out_file_name):
        response = self.stub.download(fs_pb2.Request(name=target_name))
        helpers.save_chunks_to_file(response, out_file_name)  

try:
    while True:
        option = input("press 1 to store file or 2 to search file")
        a = client()
        if option=="1":
            in_file_name = input("Enter FilePath")
            fn = in_file_name.rsplit('/',1)[1]
            print(fn)
            a.sendfile(in_file_name,fn)
        else:
            searchfile = input("Enter FileSearch")
            a.getfile(searchfile,"/home/samkit/cmpe275/Input/"+searchfile)
except KeyboardInterrupt:
        exit()

    # demo for file downloading:
    # out_file_name = '/home/samkit/cmpe275/IN/sam'
    # if os.path.exists(out_file_name):
    #     os.remove(out_file_name)
    # client.download('whatever_name', out_file_name)
    # os.system(f'sha1sum {in_file_name}')
    # os.system(f'sha1sum {out_file_name}')