import argparse
import time
from concurrent import futures

import grpc

from prometheus_client import start_http_server, Summary
from proto import namer_pb2
from proto import namer_pb2_grpc

import namer

from grpc_health.v1 import health, health_pb2, health_pb2_grpc

request_metric = Summary(
    'english_full_name_seconds',
    'Time processing EnglishFullName requests')


class Namer(namer_pb2_grpc.NamerServicer):
    @request_metric.time()
    def EnglishFullName(self, request, context):
        response = namer_pb2.NameResponse()
        first = request.first_name
        last = request.last_name
        middle = request.middle_name
        prefix = request.prefix
        suffix = request.suffix
        response.full_name = namer.english_full_name(
            first=first, last=last,
            middle=middle, prefix=prefix,
            suffix=suffix)
        # print('Peer: {}\nPeerIdentityKey: {}\nMetadata: {}'.format(
        #     context.peer(), context.peer_identity_key(),
        #     context.invocation_metadata()))
        return response


def command_args():
    parser = argparse.ArgumentParser(description='GRPC-based namer server.')
    parser.add_argument(
        '--port',
        type=int,
        required=True,
        help='The server listen port'
    )
    parser.add_argument(
        '--metrics_port',
        type=int,
        required=False,
        help='The server metrics http port'
    )
    parser.add_argument(
        '--ca_cert',
        type=str,
        required=False,
        help='CA cert or bundle.'
    )
    parser.add_argument(
        '--server_cert',
        type=str,
        required=False,
        help='Server certificate.'
    )
    parser.add_argument(
        '--server_key',
        type=str,
        required=False,
        help='Server certificate key.'
    )
    return parser.parse_args()


def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    namer_pb2_grpc.add_NamerServicer_to_server(Namer(), server)

    ca_cert = None
    client_auth = False
    if args.ca_cert:
        ca_cert = open(args.ca_cert, 'rb').read()
        client_auth = True

    if args.server_cert and args.server_key:
        private_key = open(args.server_key, 'rb').read()
        certificate_chain = open(args.server_cert, 'rb').read()

        credentials = grpc.ssl_server_credentials(
            [(private_key, certificate_chain)],
            root_certificates=ca_cert,
            require_client_auth=client_auth
        )
        server.add_secure_port('[::]:' + str(args.port), credentials)
    else:
        server.add_insecure_port('[::]:' + str(args.port))

    if args.metrics_port:
        print('Starting metrics server. Listening on port {}...'.format(
            args.metrics_port))
        start_http_server(args.metrics_port)

    print('Starting server. Listening on port {}...'.format(args.port))
    server.start()
    health_servicer.set('', health_pb2.HealthCheckResponse.SERVING)
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        health_servicer.set('', health_pb2.HealthCheckResponse.NOT_SERVING)
        time.sleep(10)
        server.stop(1)


if __name__ == '__main__':
    args = command_args()
    serve(args)
