FROM python:3.8-alpine3.10 as compile
RUN mkdir /app
WORKDIR /app
RUN apk add --no-cache curl
RUN curl -O -fssL https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.3.0/grpc_health_probe-linux-amd64 && \
    mv grpc_health_probe-linux-amd64 /usr/local/bin/grpc_health_probe && \
    chmod 755 /usr/local/bin/grpc_health_probe
RUN apk add --no-cache libstdc++
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /app
RUN apk add --no-cache --virtual build-deps build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

FROM python:3.8-alpine3.10
RUN apk add --no-cache libstdc++
RUN mkdir /app
WORKDIR /app
COPY src/ /app/
COPY --from=compile /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/namer.proto
