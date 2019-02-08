FROM python:3.7.2-alpine3.8
RUN apk add --no-cache build-base
RUN mkdir /app
COPY src/ /app/
COPY requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/namer.proto
