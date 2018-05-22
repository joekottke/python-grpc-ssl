import argparse
import time
from concurrent import futures

import grpc

import namer_pb2
import namer_pb2_grpc

import namer


class Namer(namer_pb2_grpc.NamerServicer):
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
        default=31000,
        help='The server listen port'
    )
    parser.add_argument(
        '--use_tls_auth',
        action='store_true',
        help='Enable TLS Connectivity.'
    )
    parser.add_argument(
        '--ca_cert',
        type=str,
        help='CA cert or bundle.'
    )
    parser.add_argument(
        '--server_cert',
        type=str,
        help='Server certificate.'
    )
    parser.add_argument(
        '--server_key',
        type=str,
        help='Server certificate key.'
    )
    return parser.parse_args()


def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    namer_pb2_grpc.add_NamerServicer_to_server(Namer(), server)

    if args.server_key and args.server_cert:
        private_key = open(args.server_key).read()
        certificate_chain = open(args.server_cert).read()
        if args.use_tls_auth:
            ca_cert = open(args.ca_cert).read()
            credentials = grpc.ssl_server_credentials(
                [(private_key, certificate_chain)],
                root_certificates=ca_cert,
                require_client_auth=True
            )
        else:
            credentials = grpc.ssl_server_credentials(
                [(private_key, certificate_chain)]
            )
        server.add_secure_port('[::]:' + str(args.port), credentials)
    else:
        server.add_insecure_port('[::]:' + str(args.port))
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
