# CMPE_275_DataVerse
A grpc appllication to allow distributed storage and search of files.

## Steps to Run

- Install Python3 and pip3. On Ubuntu you could execute the following command.

`apt install python3 pip3`

- From the src directory in the project install all the dependencies using the follwing command.

`pip install -r requirements.txt`

- Copy the .env-example file to create a new file named .env and enter all listed configuration values.

- Can run multiple clients using the following command.

`python ./client.py`

- Can run multiple servers using the following command.

`python ./server.py`
