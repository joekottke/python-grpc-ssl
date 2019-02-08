import argparse
import time
from concurrent import futures

import grpc

from prometheus_client import start_http_server, Summary
from proto import namer_pb2
from proto import namer_pb2_grpc

import namer

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
        print('Peer: {}\nPeerIdentityKey: {}\nMetadata: {}'.format(
            context.peer(), context.peer_identity_key(),
            context.invocation_metadata()))
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
        required=True,
        help='The server metrics http port'
    )
    parser.add_argument(
        '--ca_cert',
        type=str,
        required=True,
        help='CA cert or bundle.'
    )
    parser.add_argument(
        '--server_cert',
        type=str,
        required=True,
        help='Server certificate.'
    )
    parser.add_argument(
        '--server_key',
        type=str,
        required=True,
        help='Server certificate key.'
    )
    return parser.parse_args()


def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    namer_pb2_grpc.add_NamerServicer_to_server(Namer(), server)
    private_key = open(args.server_key,'rb').read()
    certificate_chain = open(args.server_cert,'rb').read()
    ca_cert = open(args.ca_cert,'rb').read()
    credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)],
        root_certificates=ca_cert,
        require_client_auth=True
    )
    server.add_secure_port('[::]:' + str(args.port), credentials)
    print('Starting metrics server. Listening on port {}...'.format(
        args.metrics_port))
    start_http_server(args.metrics_port)
    print('Starting server. Listening on port {}...'.format(args.port))
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    args = command_args()
    serve(args)
