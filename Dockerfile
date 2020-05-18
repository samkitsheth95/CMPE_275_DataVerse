FROM ubuntu:bionic
WORKDIR /usr/src/app
COPY . .
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt
RUN mkdir /Output


EXPOSE 8000

CMD [ "python3", "src/server.py" ]
