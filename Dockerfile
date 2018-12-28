FROM debian:9.5-slim
RUN apt-get update 
RUN apt-get -y upgrade
RUN mkdir -p /usr/share/man/man1
RUN apt-get install -y python python-pip
RUN mkdir /app
COPY src/*.py /app/
COPY proto/*.proto /app/proto/
RUN touch /app/proto/__init__.py
COPY requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./proto \
    --grpc_python_out=./proto \
    ./proto/namer.proto
