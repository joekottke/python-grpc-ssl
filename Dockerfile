FROM python:3.7.4-alpine3.10
RUN apk add --no-cache build-base
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/namer.proto
